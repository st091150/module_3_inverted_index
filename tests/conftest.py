def pytest_configure(config):
    config.option.htmlpath = "report.html"
    config.option.self_contained_html = True
