# Risk Model Assessment

This a small application that will load the trained risk model and expose a single
API `cmds/risk`.

## APIs docs

Once it is runs, go to [http://localhost:8000/docs](http://localhost:8000/docs "api documentations")

## Configuration

The risk model path is set in the config.json file.

A default json config file that is located `/code`:

```json
{
    "token_max_length": 256,
    "pre_trained_model_checkpoint": "roberta-base",
    "risk_model_path":"var/risk_model/20240107-160415_exponential/lr_2e-05_step_1/checkpoint_2.tar",
    "input_size": 768,
    "hidden_size": 768,
    "output_size": 5
}
```

This config file can be overried by mapping a custom file to `/code/config.json`.
In this case, the `var` folder has to be mapped to `/code/var` which should contain
a trained risk model.
