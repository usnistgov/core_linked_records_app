var dataId = dataId || "{{ data.data.id }}";
var oaiDataId = dataId || "{{ data.data.record_id }}";
var fedeDataId = dataId || "{{ data.data.fede_data_id }}";
var retrieveDataPidUrl = "{% url 'core_linked_records_retrieve_data_pid' %}";