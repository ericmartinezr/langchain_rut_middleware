from middleware.rut import RUTMiddleware


class TestRutDetection:
    """Tests rut detection"""

    def test_detect_rut(self):
        middleware = RUTMiddleware()
        content = "Mi rut es 17.573.28-4 y 19132501-K sin puntos"
        matches = middleware._detect(content)

        assert len(matches) == 2
        assert matches[0]["value"] == "17.573.28-4"
        assert matches[0]["start"] == 10
        assert matches[0]["end"] == 21
        assert matches[1]["value"] == "19132501-K"
        assert matches[1]["start"] == 24
        assert matches[1]["end"] == 34

    def test_not_detect_invalid_rut(self):
        middleware = RUTMiddleware()
        content = "Mi rut es 1234556-4"
        matches = middleware._detect(content)

        assert len(matches) == 0
