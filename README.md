# Shell Command Risk Assessment Model

This a small application that will load the trained risk model and expose a single
API `cmds/risk`.

The risk assessment model was trained following the work that was published in this conference paper [1].

### Citations:

[1] Touch, S., Fink, J., & Colin, J. N. (2024, November). Automated Risk Assessment of Shell-Based Attacks Using a LLM. In *International Conference on Risks and Security of Internet and Systems* (pp. 173-189). Cham: Springer Nature Switzerland.

## Docker image

* To build Docker image, run `docker compose build`. This will create two images:
    - WSGI Web application which will load the trained model
    - An Nginx web server that will do proxy pass to the WSGI application.
* To run the application, run `docker compose up -d`. This will run the web server on port `8000`.

## APIs docs

Once it is runs, go to [http://localhost:8000/docs](http://localhost:8000/docs "api documentations")

## Configuration

The risk model path is set in the `config.json` file.

A default json config file that is located `/code`:

```json
{
    "token_max_length": 256,
    "pre_trained_model_checkpoint": "roberta-base",
    "risk_model_path":"var/model/lr_2e-05_step_1/checkpoint_2.tar",
    "input_size": 768,
    "hidden_size": 768,
    "output_size": 5
}
```

This config file can be overried by mapping a custom file to `/code/config.json`.
In this case, the `var` folder has to be mapped to `/code/var` which should contain
a trained risk model.

