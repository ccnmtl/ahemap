requirejs(['./common'], function(common) {
    requirejs(['jquery', 'domReady', 'bootstrap'],
        function($, domReady, bootstrap) {
            domReady(function() {
                if (AHE.jiraConfiguration) {
                    jQuery.ajax({
                        url: AHE.jiraConfiguration,
                        type: 'get',
                        cache: true,
                        dataType: 'script'
                    });

                    window.ATL_JQ_PAGE_PROPS =  {
                        'triggerFunction': function(showCollectorDialog) {
                            jQuery('#feedback-button').click(function(e) {
                                e.preventDefault();
                                showCollectorDialog();
                            });
                        }
                    };
                }
            });
        }
    );
});
