var Step = Backbone.Model.extend({
    initialize: function () {
        // init and store our MovieCollection in our app object
        this.fields = new FieldCollection();
    }
});