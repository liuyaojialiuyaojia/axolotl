"""
CLI to run training on a model
"""
import logging
from pathlib import Path
from typing import Tuple

import fire
import transformers
from transformers import PreTrainedModel, PreTrainedTokenizer

from axolotl.cli import (
    check_accelerate_default_config,
    check_user_token,
    load_cfg,
    load_datasets,
    load_rl_datasets,
    print_axolotl_text_art,
)
from axolotl.common.cli import TrainerCliArgs
from axolotl.train import train

LOG = logging.getLogger("axolotl.cli.train")


def do_cli(config: Path = Path("examples/"), **kwargs):
    # pylint: disable=duplicate-code
    parsed_cfg = load_cfg(config, **kwargs)
    parser = transformers.HfArgumentParser((TrainerCliArgs))
    parsed_cli_args, _ = parser.parse_args_into_dataclasses(
        return_remaining_strings=True
    )
    return do_train(parsed_cfg, parsed_cli_args)


def do_train(cfg, cli_args) -> Tuple[PreTrainedModel, PreTrainedTokenizer]:
    print_axolotl_text_art()
    check_accelerate_default_config()
    check_user_token()
    if cfg.rl:
        dataset_meta = load_rl_datasets(cfg=cfg, cli_args=cli_args)
    else:
        dataset_meta = load_datasets(cfg=cfg, cli_args=cli_args)

    return train(cfg=cfg, cli_args=cli_args, dataset_meta=dataset_meta)


if __name__ == "__main__":
    fire.Fire(do_cli)
