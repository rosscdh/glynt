var FormFlowController = {
    init: function (spec) {
        // default config
        this.config = {
            connect: true
        };

        // extend our default config with passed in object attributes
        _.extend(this.config, spec);

        this.model = new FormModel({});
        this.view = new FormFlowView({model: this.model});

        this.view.model.set({'title': this.config.title});

        return this;
    },



    // any other functions here should be events handlers that respond to
    // document level events. In my case I was using this to respond to incoming XMPP
    // events. So the logic for knowing what those meant and creating or updating our
    // models and collections lived here.
    handlePubSubUpdate: function () {}
};