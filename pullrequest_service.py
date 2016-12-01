
class pullrequest_service():
    def __init__(self, pr, repo):
        self.pr = pr
        self.repo = repo


    def getLabelCount(self):
        return self.pr.labels.length


    def getchangedFiles(self):
        return self.pr.changed_files


    def checkSuccess(self):
        events = self.repo.get_issue(self.pr.number).get_events()
        close_event = next((obj for obj in events if obj.event == "closed"), None)

        return self.pr.merged or close_event.commit_id if hasattr(close_event, 'commit_id') else None


    def get_event_count(self):
        events = self.repo.get_issue(self.pr.number).get_events()
        counter = 0
        for event in events:
            counter+=1
        return counter

    
    def get_label_count(self):
        return len(self.repo.get_issue(self.pr.number).labels)


    def get_raw_data(self):
        return self.pr.raw_data
