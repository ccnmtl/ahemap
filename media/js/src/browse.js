requirejs(['./common'], function() {
    const a = ['jquery', 'bootstrap', 'Vue', 'multiselect', 'utils'];
    requirejs(a, function($, bootstrap, Vue, multiselect, utils) {
        new Vue({
            el: '#browse-container',
            components: {
                'multiselect': multiselect.Multiselect
            },
            data: function() {
                return {
                    states: utils.states,
                    state: null,
                    populations: utils.populations,
                    population: null
                };
            },
            methods: {
                onChangeCriteria: function() {
                    if (this.state) {
                        $('input[name="state"]').val(this.state.id);
                    }
                    if (this.population) {
                        $('input[name="population"]').val(this.population.id);
                    }
                },
                clearSearch: function() {
                    // eslint-disable-next-line scanjs-rules/assign_to_href
                    window.location.href = AHE.baseUrl + 'browse/';
                }
            },
            mounted: function() {
                this.$watch('state', this.onChangeCriteria);
                this.$watch('population', this.onChangeCriteria);

                const stateId = $('input[name="state"]').val();
                for (let s of this.states) {
                    if (s.id === stateId) {
                        this.state = s;
                    }
                }

                const populationId =  $('input[name="population"]').val();
                for (let p of this.populations) {
                    if (p.id === populationId) {
                        this.population = p;
                    }
                }
            }
        });
    });
});
