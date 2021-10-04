# pipen-dry

Dry runner for [pipen][1]

It is useful to quickly check is there are misconfigurations for your pipeline.

## Install

```shell
pip install -U pipen-dry
```

## Usage

- Use it for process

    ```python
    class P1(Proc):
        scheduler = "dry"
    ```

- Use it for pipeline

    ```python
    Pipen(scheduler="dry", ...)
    ```

[1]: https://github.com/pwwang/pipen
