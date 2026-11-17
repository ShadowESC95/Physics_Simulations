import ray
from ray import tune
from ray.rllib.algorithms.ppo import PPOConfig

ray.init()

tune.run(
    PPOConfig().environment("ClusterEnv").framework("torch"),
    config={
        "env_config": {
            "max_nodes": 100,
            "energy_cost": 0.01  # $/kWh
        }
    },
    stop={"training_iteration": 1000}
)
