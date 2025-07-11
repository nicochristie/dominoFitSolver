class DominoBoard:
    def __init__(self):
        self.rows = 6
        self.cols = 6
        self.blocked = set()
        self.row_targets = []
        self.col_targets = []
        self.filename = ''
        self.filepath = ''

    def to_dict(self):
        return {
            'rows': self.rows,
            'cols': self.cols,
            'blocked': list(self.blocked),
            'row_targets': self.row_targets,
            'col_targets': self.col_targets,
            'filename': self.filename,
            'filepath': self.filepath
    }
