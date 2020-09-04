var dataId = dataId || "{{ data.data.id }}";
var oaiDataId = dataId || "{{ data.data.record_id }}";
var retrieveDataPidUrl = "{% url 'core_linked_record_retrieve_data_pid_url' %}";