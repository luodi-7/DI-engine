from easydict import EasyDict

enduro_onppo_config = dict(
    exp_name='enduro_onppo_seed0',
    env=dict(
        collector_env_num=8,
        evaluator_env_num=8,
        n_evaluator_episode=8,
        stop_value=10000000000,
        env_id='EnduroNoFrameskip-v4',
        #'ALE/Enduro-v5' is available. But special setting is needed after gym make.
        frame_stack=4,
        manager=dict(shared_memory=False, )
    ),
    policy=dict(
        cuda=True,
        recompute_adv=True,
        action_space='discrete',
        model=dict(
            obs_shape=[4, 84, 84],
            action_shape=9,
            action_space='discrete',
            encoder_hidden_size_list=[32, 64, 64, 512],
            actor_head_layer_num=0,
            critic_head_layer_num=0,
            actor_head_hidden_size=512,
            critic_head_hidden_size=512,
        ),
        learn=dict(
            lr_scheduler=dict(epoch_num=5200, min_lr_lambda=0),
            epoch_per_collect=4,
            batch_size=256,
            learning_rate=2.5e-4,
            value_weight=0.5,
            entropy_weight=0.01,
            clip_ratio=0.1,
            adv_norm=True,
            value_norm=True,
            # for onppo, when we recompute adv, we need the key done in data to split traj, so we must
            # use ignore_done=False here,
            # but when we add key traj_flag in data as the backup for key done, we could choose to use ignore_done=True
            # for halfcheetah, the length=1000
            ignore_done=False,
            grad_clip_type='clip_norm',
            grad_clip_value=0.5,
        ),
        collect=dict(
            # (int) collect n_sample data, train model n_iteration times
            n_sample=1024,
            unroll_len=1,
            # (float) the trade-off factor lambda to balance 1step td and mc
            gae_lambda=0.95,
            discount_factor=0.99,
        ),
        eval=dict(evaluator=dict(eval_freq=5000, )),
    ),
)
main_config = EasyDict(enduro_onppo_config)

enduro_onppo_create_config = dict(
    env=dict(
        type='atari',
        import_names=['dizoo.atari.envs.atari_env'],
    ),
    env_manager=dict(type='subprocess'),
    policy=dict(type='ppo'),
)
create_config = EasyDict(enduro_onppo_create_config)

if __name__ == '__main__':
    # or you can enter ding -m serial_onpolicy -c enduro_onppo_config.py -s 0
    from ding.entry import serial_pipeline_onpolicy
    serial_pipeline_onpolicy((main_config, create_config), seed=0)
