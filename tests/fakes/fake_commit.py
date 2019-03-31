class FakeCommit:
    def __init__(self, committed_datetime, hexsha):
        self._committed_datetime = committed_datetime
        self._hexsha = hexsha
        self._stats = None

    @property
    def committed_datetime(self):
        """Return the value of current student."""
        return self._committed_datetime

    @committed_datetime.setter
    def committed_datetime(self, committed_datetime):
        """Set the value of current student."""
        self._committed_datetime = committed_datetime

    @property
    def hexsha(self):
        """Return the value of current student."""
        return self._hexsha

    @hexsha.setter
    def hexsha(self, hexsha):
        """Set the value of current student."""
        self._hexsha = hexsha

    @property
    def stats(self):
        """Return the value of current student."""
        return self._stats

    @stats.setter
    def stats(self, stats):
        """Set the value of current student."""
        self._stats = stats


class FakeStats:
    def __init__(self, fileneme, insertions, deletions):
        # insertions = record.stats.files[selected_file]["insertions"]
        self._files = {fileneme: {"insertions": insertions, "deletions": deletions}}

    @property
    def files(self):
        """Return the value of current student."""
        return self._files

    @files.setter
    def files(self, files):
        """Set the value of current student."""
        self._files = files
