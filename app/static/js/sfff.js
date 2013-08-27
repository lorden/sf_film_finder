$(document).foundation();

// Preload loading gif
i = new Image();
i.src = 'static/img/loading.gif';

var finder = {
    // main app
}

// Router
finder.Router = Backbone.Router.extend({

    routes: {
        "": "home",
        "movies/:id": "movieDetails",
    },

    home: function(){
        finder.searchView = new finder.SearchView();
        $('#results').html(finder.searchView.render());
    },

    movieDetails: function(id){
        finder.movieView = new finder.movieView({model: new finder.Movie({id: id})});
        finder.movieView.render();
    },

    showIntro: function(){
        $('#intro').slideDown();
        $('#search').focus();
    },

    hideIntro: function(){
        $('#intro').slideUp();
    },

    loading: function(){
        $('#loading').slideUp();
        var template = _.template($('#loading-template').html(), {
            term: this.term,
        });
        $('#results').html(template);
    },

});

// Models
finder.Movie = Backbone.Model.extend({

    el: '#results',

    urlRoot: "/movies"

});

// Collections
finder.MovieList = Backbone.Collection.extend({

    url: "/movies",

    model: finder.Movie

});

// Views
finder.movieView = Backbone.View.extend({

    el: '#results',

    initialize: function(){
        this.model.fetch();
        this.listenTo(this.model, "change", this.render);
    },

    render: function(){
        finder.router.hideIntro();
        var self = this;
        var template = _.template($('#movie-template').html(), {
            movie: self.model
        });
        self.$el.html(template);
        return this;
    }
});

finder.SearchView = Backbone.View.extend({

    term: '',

    el: '#results',

    initialize: function(){
        this.results = new finder.MovieList();
    },

    events: {
        "keyup #search": "searchTimer",
        "click .search-movie": "showMovie"
    },

    searchTimer: function(){
        var self = this;
        if(this.timer){
            clearTimeout(this.timer);
        }
        this.timer = setTimeout(function() {
            self.search();
            self.timer = null;
        }, 500);
    },
    
    search: function(){
        var self = this;
        var q = $('#search').val();
        if (q == '') {
            this.term = q;
            this.results.reset();
            this.render();
            finder.router.showIntro();
        }
        else if(this.term == q) {
            return;
        } else {
            finder.router.loading();
            finder.router.hideIntro();
            this.results.fetch({
                data: {q: q},
                success: function(){
                    self.render();
                }
            });
            this.term = q;
        }
    },

    render: function(){
        var template = _.template($('#movie-list-template').html(), {
            movies: this.results.models,
            term: this.term
        });
        this.$el.html(template);
    },

});


$(document).on('ready', function(){
    finder.router = new finder.Router();
    Backbone.history.start();
});
