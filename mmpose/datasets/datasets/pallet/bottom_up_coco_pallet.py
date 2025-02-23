# Copyright (c) OpenMMLab. All rights reserved.
import os
import warnings
from collections import OrderedDict, defaultdict

import json_tricks as json
import numpy as np
from mmcv import Config
from xtcocotools.cocoeval import COCOeval

from mmpose.core.post_processing import oks_nms, soft_oks_nms
from mmpose.datasets.builder import DATASETS
from mmpose.datasets.datasets.base import Kpt2dSviewRgbImgBottomUpDataset


@DATASETS.register_module()
class BottomUpCocoPalletDataset(Kpt2dSviewRgbImgBottomUpDataset):

    def __init__(self,
                 ann_file,
                 img_prefix,
                 data_cfg,
                 pipeline,
                 dataset_info=None,
                 test_mode=False):

        if dataset_info is None:
            warnings.warn(
                'dataset_info is missing. '
                'Check https://github.com/open-mmlab/mmpose/pull/663 '
                'for details.', DeprecationWarning)
            cfg = Config.fromfile('configs/_base_/datasets/coco.py')
            dataset_info = cfg._cfg_dict['dataset_info']

        super().__init__(
            ann_file,
            img_prefix,
            data_cfg,
            pipeline,
            dataset_info=dataset_info,
            test_mode=test_mode)

        self.ann_info['use_different_joint_weights'] = False
        print(f'=> num_images: {self.num_images}')

    def _get_single(self, idx):
        """Get anno for a single image.

        Args:
            idx (int): image idx

        Returns:
            dict: info for model training
        """
        coco = self.coco
        img_id = self.img_ids[idx]
        ann_ids = coco.getAnnIds(imgIds=img_id)
        anno = coco.loadAnns(ann_ids)

        mask = self._get_mask(anno, idx)
        anno = [
            obj.copy() for obj in anno
            if obj['iscrowd'] == 0 or obj['num_keypoints'] > 0
        ]

        joints = self._get_joints(anno)
        mask_list = [mask.copy() for _ in range(self.ann_info['num_scales'])]
        joints_list = [
            joints.copy() for _ in range(self.ann_info['num_scales'])
        ]

        db_rec = {}
        db_rec['dataset'] = self.dataset_name
        db_rec['image_file'] = os.path.join(self.img_prefix,
                                            self.id2name[img_id])
        db_rec['mask'] = mask_list
        db_rec['joints'] = joints_list

        return db_rec

    def _get_joints(self, anno):
        """Get joints for all people in an image."""
        num_people = len(anno)

        if self.ann_info['scale_aware_sigma']:
            joints = np.zeros((num_people, self.ann_info['num_joints'], 4),
                              dtype=np.float32)
        else:
            joints = np.zeros((num_people, self.ann_info['num_joints'], 3),
                              dtype=np.float32)

        for i, obj in enumerate(anno):
            joints[i, :, :3] = \
                np.array(obj['keypoints']).reshape([-1, 3])
            if self.ann_info['scale_aware_sigma']:
                # get person box
                box = obj['bbox']
                size = max(box[2], box[3])
                sigma = size / self.base_size * self.base_sigma
                if self.int_sigma:
                    sigma = int(np.ceil(sigma))
                assert sigma > 0, sigma
                joints[i, :, 3] = sigma

        return joints

    def evaluate(self, outputs, res_folder, metric='mAP', **kwargs):
        """Evaluate coco keypoint results. The pose prediction results will be
        saved in `${res_folder}/result_keypoints.json`.

        Note:
            num_people: P
            num_keypoints: K

        Args:
            outputs (list(preds, scores, image_path, heatmap)):

                * preds (list[np.ndarray(P, K, 3+tag_num)]):
                  Pose predictions for all people in images.
                * scores (list[P]):
                * image_path (list[str]): For example, ['coco/images/
                val2017/000000397133.jpg']
                * heatmap (np.ndarray[N, K, H, W]): model outputs.

            res_folder (str): Path of directory to save the results.
            metric (str | list[str]): Metric to be performed. Defaults: 'mAP'.

        Returns:
            dict: Evaluation results for evaluation metric.
        """
        metrics = metric if isinstance(metric, list) else [metric]
        allowed_metrics = ['mAP']
        for metric in metrics:
            if metric not in allowed_metrics:
                raise KeyError(f'metric {metric} is not supported')

        res_file = os.path.join(res_folder, 'result_keypoints.json')

        preds = []
        scores = []
        image_paths = []

        for output in outputs:
            preds.append(output['preds'])
            scores.append(output['scores'])
            image_paths.append(output['image_paths'][0])

        kpts = defaultdict(list)
        # iterate over images
        for idx, _preds in enumerate(preds):
            str_image_path = image_paths[idx]
            image_id = self.name2id[os.path.basename(str_image_path)]
            # iterate over people
            for idx_person, kpt in enumerate(_preds):
                # use bbox area
                area = (np.max(kpt[:, 0]) - np.min(kpt[:, 0])) * (
                    np.max(kpt[:, 1]) - np.min(kpt[:, 1]))

                kpts[image_id].append({
                    'keypoints': kpt[:, 0:3],
                    'score': scores[idx][idx_person],
                    'tags': kpt[:, 3],
                    'image_id': image_id,
                    'area': area,
                })

        valid_kpts = []
        for img in kpts.keys():
            img_kpts = kpts[img]
            if self.use_nms:
                nms = soft_oks_nms if self.soft_nms else oks_nms
                keep = nms(img_kpts, self.oks_thr, sigmas=self.sigmas)
                valid_kpts.append([img_kpts[_keep] for _keep in keep])
            else:
                valid_kpts.append(img_kpts)

        self._write_coco_keypoint_results(valid_kpts, res_file)

        info_str = self._do_python_keypoint_eval(res_file)
        name_value = OrderedDict(info_str)
        return name_value

    def _write_coco_keypoint_results(self, keypoints, res_file):
        """Write results into a json file."""
        data_pack = [{
            'cat_id': self._class_to_coco_ind[cls],
            'cls_ind': cls_ind,
            'cls': cls,
            'ann_type': 'keypoints',
            'keypoints': keypoints
        } for cls_ind, cls in enumerate(self.classes)
                     if not cls == '__background__']

        results = self._coco_keypoint_results_one_category_kernel(data_pack[0])

        with open(res_file, 'w') as f:
            json.dump(results, f, sort_keys=True, indent=4)

    def _coco_keypoint_results_one_category_kernel(self, data_pack):
        """Get coco keypoint results."""
        cat_id = data_pack['cat_id']
        keypoints = data_pack['keypoints']
        cat_results = []

        for img_kpts in keypoints:
            if len(img_kpts) == 0:
                continue

            _key_points = np.array(
                [img_kpt['keypoints'] for img_kpt in img_kpts])
            key_points = _key_points.reshape(-1,
                                             self.ann_info['num_joints'] * 3)

            for img_kpt, key_point in zip(img_kpts, key_points):
                kpt = key_point.reshape((self.ann_info['num_joints'], 3))
                left_top = np.amin(kpt, axis=0)
                right_bottom = np.amax(kpt, axis=0)

                w = right_bottom[0] - left_top[0]
                h = right_bottom[1] - left_top[1]

                cat_results.append({
                    'image_id': img_kpt['image_id'],
                    'category_id': cat_id,
                    'keypoints': key_point.tolist(),
                    'score': img_kpt['score'],
                    'bbox': [left_top[0], left_top[1], w, h]
                })

        return cat_results

    def _do_python_keypoint_eval(self, res_file):
        """Keypoint evaluation using COCOAPI."""

        stats_names = [
            'AP', 'AP .5', 'AP .75', 'AP (M)', 'AP (L)', 'AR', 'AR .5',
            'AR .75', 'AR (M)', 'AR (L)'
        ]

        with open(res_file, 'r') as file:
            res_json = json.load(file)
            if not res_json:
                info_str = list(zip(stats_names, [
                    0,
                ] * len(stats_names)))
                return info_str

        coco_det = self.coco.loadRes(res_file)
        coco_eval = COCOeval(self.coco, coco_det, 'keypoints', self.sigmas)
        coco_eval.params.useSegm = None
        coco_eval.evaluate()
        coco_eval.accumulate()
        coco_eval.summarize()

        info_str = list(zip(stats_names, coco_eval.stats))

        return info_str
