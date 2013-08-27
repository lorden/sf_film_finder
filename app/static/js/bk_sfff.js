$(document).foundation();

$(document).ready(function(){
    $('#search').on('keyup', function(){
        if($('#intro').is(':visible')) {
            $('#intro').fadeOut();
        }
        if($(this).val().length > 2) {
            location.href = '/#/search/' + $(this).val();
        }
    });
    
});

$(function(){

    var Movie = Backbone.Model.extend({
        urlRoot: '/movies/',

    });

    var Movies = Backbone.Collection.extend({
        url: '/search/',
        model: Movie,
        initialize: function(term){
            this.url += term;
        }
    });

    var MovieList = Backbone.View.extend({
        el: '#results',
        events: {
            'click': 'open'
        },
        render: function(){
            var that = this;
            var movies = new Movies();
            movies.fetch({
                success: function(movies){
                    console.log(movies);
                    var template = _.template($('#movie-list-template').html(), {movies: movies.models});
                    that.$el.html(template);
                }
            });
        },
        search: function(term){
            var movies = new Movies(term);
            var that = this;
            movies.fetch({
                success: function(movies){
                    console.log(movies);
                    var template = _.template($('#movie-list-template').html(), {movies: movies.models});
                    that.$el.html(template);
                }
            });
        },
        open: function() {
            console.log('open movie');
            console.log(this.model);
            console.log(router);
        }
    });

    var movieList = new MovieList();

    var Router = Backbone.Router.extend({
        routes: {
            '': 'home',
            'search/:term': 'search'
        }
    });

    var router = new Router();
    router.on('route:home', function() {
        console.log('route home!');
        // movieList.render();
    });

    router.on('route:search', function(term) {
        movieList.search(term);
    });

    Backbone.history.start();


});
