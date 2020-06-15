class RankCalculate:
    def __init__(self, query, request):
        self.query = query
        self.request = request

    def AddNewRank(self):
        vote_count = self.query.vote_count
        vote_avg = self.query.vote_average
        total = vote_count * vote_avg
        self.query.vote_average = round((total + int(self.request.data['rank'])) / (vote_count + 1), 1)
        self.query.vote_count = vote_count + 1
        self.query.save()

    def UpdateNewRank(self,prev_rank):
        movie = self.query.movie
        vote_count = movie.vote_count
        vote_avg = movie.vote_average
        total = vote_count * vote_avg
        movie.vote_average = round((total - int(prev_rank) + int(self.request.data['rank'])) / vote_count, 1)
        movie.save()

    def DeleteRank(self,prev_rank):
        movie = self.query.movie
        vote_count = movie.vote_count
        vote_avg = movie.vote_average
        total = vote_count * vote_avg
        movie.vote_average = round((total - int(prev_rank)) / (vote_count - 1), 1)
        movie.vote_count -= 1
        movie.save()