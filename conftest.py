def pytest_addoption(parser):
    parser.addoption(
        "--integration", action="store_true", dest="integration", default=False, help="Run integration tests"
    )


def pytest_collection_modifyitems(config):
    if config.option.integration:
        setattr(config.option, "markexpr", "integration")
    else:
        setattr(config.option, "markexpr", "not integration")
