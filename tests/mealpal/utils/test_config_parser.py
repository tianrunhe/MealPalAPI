def test_decrypt(config_fetcher):
    assert config_fetcher.get_account_info() == {
        "email": "tianrunhe@gmail.com",
        "encryptedPassword": 'AQICAHhSkpLPt8hfBIFOlpUap2QGsB88EYL1GoVPqMsUM4fs0AEBRQ8geAWntrKuJrnvel4DAAAAbTBrBgkqhkiG9w0BBwagXjBcAgEAMFcGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMTy5jeHKN0iuk3OWvAgEQgCpm3+E2P+95kmjDThSUXva9UqxmUQcitMnT5OYgUjev5PQpJF2pwNiWxcU='
    }
