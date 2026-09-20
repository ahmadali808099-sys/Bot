import asyncio
import re

from config import SSHX_COMMAND


class SSHXManager:
    """
    Creates a temporary SSHX web-terminal session on a VPS
    and extracts the generated URL from the command output.
    """

    URL_PATTERN = re.compile(
        r"https?://[^\s<>\"]+",
        re.IGNORECASE,
    )

    async def create_session(self, run_command):
        """
        run_command must be a callable that executes a command
        inside the target VPS and returns:
            {
                "returncode": int,
                "stdout": str,
                "stderr": str
            }
        """

        result = await run_command(SSHX_COMMAND)

        output = "\n".join(
            [
                result.get("stdout", ""),
                result.get("stderr", ""),
            ]
        )

        if result.get("returncode", 1) != 0:
            raise RuntimeError(
                "SSHX command failed:\n" + output[-1500:]
            )

        urls = self.URL_PATTERN.findall(output)

        if not urls:
            raise RuntimeError(
                "SSHX did not return a web-terminal URL."
            )

        # Prefer an SSHX URL when multiple URLs are printed.
        for url in urls:
            if "sshx.io" in url.lower():
                return url.rstrip(".,);]")

        return urls[0].rstrip(".,);]")


sshx_manager = SSHXManager()
