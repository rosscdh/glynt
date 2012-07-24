var FormFlowView = Backbone.View.extend({
    initialize: function (args) {
        _.bindAll(this, 'changeTitle');
        this.model.bind('change:title', this.changeTitle);
    },

    events: {
        'click #form_title': 'handleTitleClick'
    },


    render: function () {
        // "ich" is ICanHaz.js magic
        this.el = ich.app(this.model.toJSON());
        return this;
    },

    changeTitle: function () {
        this.$('#form_title').text(this.model.get('title'));
    },

    handleTitleClick: function () {
        alert('you clicked the title: ' + this.model.get('title'));
    }
});