_base_ = ['../../../../_base_/datasets/pallet.py']
log_level = 'INFO'
load_from = None
resume_from = None
dist_params = dict(backend='nccl')
workflow = [('train', 1)]
checkpoint_config = dict(interval=25)
evaluation = dict(interval=25, metric='mAP', save_best='AP')

optimizer = dict(
    type='Adam',
    lr=1e-5,
)
optimizer_config = dict(grad_clip=None)
# learning policy
lr_config = dict(
    policy='step',
    warmup='linear',
    warmup_iters=500,
    warmup_ratio=0.001,
    step=[200, 260])
total_epochs = 300
log_config = dict(
    interval=50,
    hooks=[
        dict(type='TextLoggerHook'),
        # dict(type='TensorboardLoggerHook')
    ])

channel_cfg = dict(
    num_output_channels=16, 
    dataset_joints=16,
    dataset_channel=[
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 15],
    ],
    inference_channel=[
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 15
    ])

data_cfg = dict(
    image_size=512,
    base_size=256,
    base_sigma=2,
    heatmap_size=[128],
    num_joints=channel_cfg['dataset_joints'],
    dataset_channel=channel_cfg['dataset_channel'],
    inference_channel=channel_cfg['inference_channel'],
    num_scales=1,
    scale_aware_sigma=False,
)

# model settings
model = dict(
    type='AssociativeEmbedding',
    pretrained=None,
    backbone=dict(
        type='HourglassAENet',
        num_stacks=4,
        out_channels=32,
    ),
    keypoint_head=dict(
        type='AEMultiStageHead',
        in_channels=32,
        out_channels=32,
        num_stages=4,
        num_deconv_layers=0,
        extra=dict(final_conv_kernel=0),
        loss_keypoint=dict(
            type='MultiLossFactory',
            num_joints=16,
            num_stages=4,
            ae_loss_type='exp',
            with_heatmaps_loss=[True, True, True, True],
            with_ae_loss=[True, True, True, True],
            push_loss_factor=[1.0, 1.0, 1.0, 1.0],
            pull_loss_factor=[1.0, 1.0, 1.0, 1.0],
            heatmaps_loss_factor=[1.0, 1.0, 1.0, 1.0])),
    train_cfg=dict(
        num_joints=channel_cfg['dataset_joints'],
        img_size=data_cfg['image_size']),
    test_cfg=dict(
        num_joints=channel_cfg['dataset_joints'],
        max_num_people=30,
        scale_factor=[1],
        with_heatmaps=[True, True, True, True],
        with_ae=[True, True, True, True],
        select_output_index=[3],
        project2image=True,
        nms_kernel=5,
        nms_padding=2,
        tag_per_joint=True,
        detection_threshold=0.1,
        tag_threshold=1,
        use_detection_val=True,
        ignore_too_much=False,
        adjust=True,
        refine=True,
        flip_test=True))

train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='BottomUpRandomAffine',
        rot_factor=30,
        scale_factor=[0.75, 1.5],
        scale_type='short',
        trans_factor=40),
    dict(type='BottomUpRandomFlip', flip_prob=0.5),
    dict(type='ToTensor'),
    dict(
        type='NormalizeTensor',
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]),
    dict(
        type='MultitaskGatherTarget',
        pipeline_list=[
            [dict(type='BottomUpGenerateTarget', sigma=2, max_num_people=30)],
        ],
        pipeline_indices=[0] * 4,
        keys=['targets', 'masks', 'joints']),
    dict(
        type='Collect',
        keys=['img', 'joints', 'targets', 'masks'],
        meta_keys=[]),
]

val_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='BottomUpGetImgSize', test_scale_factor=[1]),
    dict(
        type='BottomUpResizeAlign',
        transforms=[
            dict(type='ToTensor'),
            dict(
                type='NormalizeTensor',
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]),
        ]),
    dict(
        type='Collect',
        keys=['img'],
        meta_keys=[
            'image_file', 'aug_data', 'test_scale_factor', 'base_size',
            'center', 'scale', 'flip_index'
        ]),
]

test_pipeline = val_pipeline

data_root = '/home/arhimede/Desktop/bairam/datasets/e2e_keypoint'
data = dict(
    samples_per_gpu=6,
    workers_per_gpu=2,
    train=dict(
        type='BottomUpCocoPalletDataset',
        ann_file=f'{data_root}/annotations/coco/pallet_keypoints_coco_train.json',
        img_prefix=f'{data_root}/images/train/',
        data_cfg=data_cfg,
        pipeline=train_pipeline,
        dataset_info={{_base_.dataset_info}}),
    val=dict(
        type='BottomUpCocoPalletDataset',
        ann_file=f'{data_root}/annotations/coco/pallet_keypoints_coco_val.json',
        img_prefix=f'{data_root}/images/val/',
        data_cfg=data_cfg,
        pipeline=val_pipeline,
        dataset_info={{_base_.dataset_info}}),
    test=dict(
        type='BottomUpCocoPalletDataset',
        ann_file=f'{data_root}/annotations/coco/pallet_keypoints_coco_val.json',
        img_prefix=f'{data_root}/imagse/val/',
        data_cfg=data_cfg,
        pipeline=test_pipeline,
        dataset_info={{_base_.dataset_info}}),
)
