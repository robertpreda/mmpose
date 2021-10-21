dataset_info = dict(
    dataset_name='pp',
    paper_info=dict(
        
    ),
    keypoint_info={
        0:
        dict(name='products_far_left_top', id=0, color=[51, 153, 255], type='upper', swap='products_far_right_top'),
        1:
        dict(
            name='products_far_left_bottom',
            id=1,
            color=[51, 153, 255],
            type='upper',
            swap='products_far_right_bottom'),
        2:
        dict(
            name='products_far_right_top',
            id=2,
            color=[51, 153, 255],
            type='upper',
            swap='products_far_left_top'),
        3:
        dict(
            name='products_far_right_bottom',
            id=3,
            color=[51, 153, 255],
            type='upper',
            swap='products_far_left_bottom'),
        4:
        dict(
            name='products_near_left_top',
            id=4,
            color=[51, 153, 255],
            type='upper',
            swap='products_near_right_top'),
        5:
        dict(
            name='products_near_left_bottom',
            id=5,
            color=[0, 255, 0],
            type='upper',
            swap='products_near_right_bottom'),
        6:
        dict(
            name='products_near_right_top',
            id=6,
            color=[255, 128, 0],
            type='upper',
            swap='products_near_left_top'),
        7:
        dict(
            name='products_near_right_bottom',
            id=7,
            color=[0, 255, 0],
            type='upper',
            swap='products_near_left_bottom'),
        8:
        dict(
            name='pallet_far_left_top',
            id=8,
            color=[255, 128, 0],
            type='lower',
            swap='pallet_far_right_top'),
        9:
        dict(
            name='pallet_far_left_bottom',
            id=9,
            color=[0, 255, 0],
            type='lower',
            swap='pallet_far_right_bottom'),
        10:
        dict(
            name='pallet_far_right_top',
            id=10,
            color=[255, 128, 0],
            type='lower',
            swap='pallet_far_left_top'),
        11:
        dict(
            name='pallet_far_right_bottom',
            id=11,
            color=[0, 255, 0],
            type='lower',
            swap='pallet_far_left_bottom'),
        12:
        dict(
            name='pallet_near_left_top',
            id=12,
            color=[255, 128, 0],
            type='lower',
            swap='pallet_near_right_top'),
        13:
        dict(
            name='pallet_near_left_bottom',
            id=13,
            color=[0, 255, 0],
            type='lower',
            swap='pallet_near_right_bottom'),
        14:
        dict(
            name='pallet_near_right_top',
            id=14,
            color=[255, 128, 0],
            type='lower',
            swap='pallet_near_left_top'),
        15:
        dict(
            name='pallet_near_right_bottom',
            id=15,
            color=[0, 255, 0],
            type='lower',
            swap='pallet_near_left_bottom')
    },
    skeleton_info={
        0:
        dict(link=('products_far_left_top', 'products_far_left_bottom'), id=0, color=[0, 255, 0]),
        1:
        dict(link=('products_far_left_bottom', 'products_near_left_bottom'), id=1, color=[0, 255, 0]),
        2:
        dict(link=('products_near_left_bottom', 'products_near_left_top'), id=2, color=[255, 128, 0]),
        3:
        dict(link=('products_near_left_top', 'products_far_left_top'), id=3, color=[255, 128, 0]),
        4:
        dict(link=('products_far_left_top', 'products_far_right_top'), id=4, color=[51, 153, 255]),
        5:
        dict(link=('products_far_right_top', 'products_far_right_bottom'), id=5, color=[51, 153, 255]),
        6:
        dict(link=('products_far_right_bottom', 'products_far_left_bottom'), id=6, color=[51, 153, 255]),
        7:
        dict(
            link=('products_far_right_bottom', 'products_near_right_bottom'),
            id=7,
            color=[51, 153, 255]),
        8:
        dict(link=('products_near_right_bottom', 'products_near_right_top'), id=8, color=[0, 255, 0]),
        9:
        dict(
            link=('products_near_right_bottom', 'products_near_left_bottom'), id=9, color=[255, 128, 0]),
        10:
        dict(link=('products_near_left_top', 'products_near_right_top'), id=10, color=[0, 255, 0]),
        11:
        dict(link=('products_near_right_top', 'products_far_right_top'), id=11, color=[255, 128, 0]),
       12:
        dict(link=('pallet_far_left_top', 'pallet_far_left_bottom'), id=12, color=[0, 255, 0]),
        13:
        dict(link=('pallet_far_left_bottom', 'pallet_near_left_bottom'), id=13, color=[0, 255, 0]),
        14:
        dict(link=('pallet_near_left_bottom', 'pallet_near_left_top'), id=14, color=[255, 128, 0]),
        15:
        dict(link=('pallet_near_left_top', 'pallet_far_left_top'), id=15, color=[255, 128, 0]),
        16:
        dict(link=('pallet_far_left_top', 'pallet_far_right_top'), id=16, color=[51, 153, 255]),
        17:
        dict(link=('pallet_far_right_top', 'pallet_far_right_bottom'), id=17, color=[51, 153, 255]),
        18:
        dict(link=('pallet_far_right_bottom', 'pallet_far_left_bottom'), id=17, color=[51, 153, 255]),
        19:
        dict(
            link=('pallet_far_right_bottom', 'pallet_near_right_bottom'),
            id=19,
            color=[51, 153, 255]),
        20:
        dict(link=('pallet_near_right_bottom', 'products_near_right_top'), id=20, color=[0, 255, 0]),
        21:
        dict(
            link=('pallet_near_right_bottom', 'pallet_near_left_bottom'), id=21, color=[255, 128, 0]),
        22:
        dict(link=('pallet_near_left_top', 'pallet_near_right_top'), id=22, color=[0, 255, 0]),
        23:
        dict(link=('pallet_near_right_top', 'pallet_far_right_top'), id=23, color=[255, 128, 0]),
    },
    joint_weights=[
        1., 1., 1., 1., 1., 1., 1., 1.2, 1.2, 1.5, 1.5, 1., 1., 1.2, 1.2, 1.5,
    ],
    sigmas=[
        0.026, 0.025, 0.025, 0.035, 0.035, 0.079, 0.079, 0.072, 0.072, 0.062,
        0.062, 0.107, 0.107, 0.087, 0.087, 0.089
    ])
