# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

from pathlib import Path

from llama_stack.distribution.datatypes import ModelInput, Provider, ShieldInput
from llama_stack.providers.inline.inference.meta_reference import (
    MetaReferenceInferenceConfig,
)
from llama_stack.templates.template import DistributionTemplate, RunConfigSettings


def get_distribution_template() -> DistributionTemplate:
    providers = {
        "inference": ["inline::meta-reference"],
        "memory": ["inline::faiss", "remote::chromadb", "remote::pgvector"],
        "safety": ["inline::llama-guard"],
        "agents": ["inline::meta-reference"],
        "telemetry": ["inline::meta-reference"],
    }

    inference_provider = Provider(
        provider_id="meta-reference-inference",
        provider_type="inline::meta-reference",
        config=MetaReferenceInferenceConfig.sample_run_config(
            model="${env.INFERENCE_MODEL}",
            checkpoint_dir="${env.INFERENCE_CHECKPOINT_DIR:null}",
        ),
    )

    inference_model = ModelInput(
        model_id="${env.INFERENCE_MODEL}",
        provider_id="meta-reference-inference",
    )
    safety_model = ModelInput(
        model_id="${env.SAFETY_MODEL}",
        provider_id="meta-reference-safety",
    )

    return DistributionTemplate(
        name="meta-reference-gpu",
        distro_type="self_hosted",
        description="Use Meta Reference for running LLM inference",
        template_path=Path(__file__).parent / "doc_template.md",
        providers=providers,
        default_models=[inference_model, safety_model],
        run_configs={
            "run.yaml": RunConfigSettings(
                provider_overrides={
                    "inference": [inference_provider],
                },
                default_models=[inference_model],
            ),
            "run-with-safety.yaml": RunConfigSettings(
                provider_overrides={
                    "inference": [
                        inference_provider,
                        Provider(
                            provider_id="meta-reference-safety",
                            provider_type="inline::meta-reference",
                            config=MetaReferenceInferenceConfig.sample_run_config(
                                model="${env.SAFETY_MODEL}",
                                checkpoint_dir="${env.SAFETY_CHECKPOINT_DIR:null}",
                            ),
                        ),
                    ],
                },
                default_models=[
                    inference_model,
                    safety_model,
                ],
                default_shields=[ShieldInput(shield_id="${env.SAFETY_MODEL}")],
            ),
        },
        run_config_env_vars={
            "LLAMASTACK_PORT": (
                "5001",
                "Port for the Llama Stack distribution server",
            ),
            "INFERENCE_MODEL": (
                "meta-llama/Llama-3.2-3B-Instruct",
                "Inference model loaded into the Meta Reference server",
            ),
            "INFERENCE_CHECKPOINT_DIR": (
                "null",
                "Directory containing the Meta Reference model checkpoint",
            ),
            "SAFETY_MODEL": (
                "meta-llama/Llama-Guard-3-1B",
                "Name of the safety (Llama-Guard) model to use",
            ),
            "SAFETY_CHECKPOINT_DIR": (
                "null",
                "Directory containing the Llama-Guard model checkpoint",
            ),
        },
    )
