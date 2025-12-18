import re
from langchain.agents.middleware import PIIMiddleware
from langchain.agents.middleware._redaction import PIIMatch

DASHES = "\u002D\u2011\u2013\u2212"


class RUTMiddleware(PIIMiddleware):
    def __init__(self, rut_pattern: str | None = None, **kwargs):
        """
        Initialize the RUT middleware

        Args:
            rut_pattern (str, optional): Regex pattern to capture ruts
        """

        if rut_pattern is None:
            rut_pattern = r"\b\d{7,8}\-[0-9Kk]\b|\b\d{1,2}\.\d{3}\.\d{2,3}\-[0-9Kk]\b"

        self.pii_type = "rut"
        self.rut_pattern = rut_pattern

        super().__init__(pii_type=self.pii_type, detector=self._detect, **kwargs)

    def _normalize_content(self, content: str) -> str:
        """
        Normalize the content.


        Converts the following hyphens to the common one U+002D
        U+2011 - Non-breaking hyphen
        U+2013 - En dash
        U+2212 - Minus sign

        Args:
            content (str): Content to be normalized

        Returns:
            Content normalized
        """
        return re.sub(f"[{DASHES}]", "\u002D", content)

    def _is_valid(self, rut: str) -> bool:
        """
        Checks if the rut found is valid

        Args:
            rut (str): rut found

        Returns:
            If the rut found is valid or not
        """
        rut_sin_dv = rut.split('-')[0].replace(".", "")
        dv = rut[-1].strip().lower()
        dv_pos = [str(num) for num in range(0, 10)] + ["k"]

        if dv not in dv_pos:
            return False

        serie = 2
        sum = 0
        for dig in reversed(rut_sin_dv):
            if serie == 8:
                serie = 2

            sum += int(dig) * serie
            serie += 1

        dv_calc = 11 - (sum - ((sum // 11) * 11))
        return dv == ("k" if str(dv_calc) == "10" else str(dv_calc))

    def _detect(self, content: str) -> list[PIIMatch]:
        """
        Finds ruts in the content

        Args:
            content (str): Content where to look for ruts

        Returns:
            List if ruts found
        """
        matches = []
        content = self._normalize_content(content)
        for match in re.finditer(self.rut_pattern, content):
            value = match.group()
            if self._is_valid(value):
                matches.append(
                    PIIMatch(
                        type=self.pii_type,
                        value=value,
                        start=match.start(),
                        end=match.end()
                    )
                )

        return matches
