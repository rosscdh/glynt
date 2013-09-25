casper.test.comment(casper.cli.options.test_label);

var helper = require(casper.cli.options.casper_helper_js_path);

helper.scenario(casper.cli.options.url,
    function() {
        //this.echo(this.debugHTML())
        this.test.assertHttpStatus(200);
        this.test.assertTitle('Overview')
        this.test.assertSelectorHasText('h1', 'Your LawPal Projects', 'Header Text on Page')
        
        this.test.assertExists('table#lawyer-projects')
        this.test.assertSelectorHasText('table#lawyer-projects th:nth-child(1)', 'Company')
        this.test.assertSelectorHasText('table#lawyer-projects th:nth-child(2)', 'Client Contact')
        this.test.assertSelectorHasText('table#lawyer-projects th:nth-child(3)', 'Status')

        this.test.assertElementCount('table#lawyer-projects tr.project-list-item', 1)
        this.test.assertElementCount('table#lawyer-projects tr.project-list-item td', 5)
        
        this.test.assertExists('table#lawyer-projects tr.project-list-item td:nth-child(2) div.profile-card[data-template="small"][data-username="customer"]')

        /**
        * Test the row properties for the proposed lawyer
        */
        this.test.assertSelectorHasText('table#lawyer-projects tr.project-list-item td:nth-child(3) a[data-toggle="modal"][data-target="#overview-modal"][data-is_ajax="true"]', 'Discuss')
        this.test.assertSelectorHasText('table#lawyer-projects tr.project-list-item td:nth-child(4) strong', 'Proposed')
        this.test.assertSelectorHasText('table#lawyer-projects tr.project-list-item td:nth-child(5) small', 'You have been proposed to this client. Awaiting client decision. Press the Discuss link to send a message directly to them.')
    }
);

helper.run();