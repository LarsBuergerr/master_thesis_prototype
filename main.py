import hydra
from omegaconf import DictConfig, OmegaConf

from src.analyser import Analyser

import logging
logging.basicConfig(level=logging.INFO)


@hydra.main(version_base=None, config_path="conf")
def my_app(cfg : DictConfig) -> None:
    logging.info(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    my_app()