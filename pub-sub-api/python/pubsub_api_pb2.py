# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: pubsub_api.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'pubsub_api.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10pubsub_api.proto\x12\x0b\x65ventbus.v1\"\x83\x01\n\tTopicInfo\x12\x12\n\ntopic_name\x18\x01 \x01(\t\x12\x13\n\x0btenant_guid\x18\x02 \x01(\t\x12\x13\n\x0b\x63\x61n_publish\x18\x03 \x01(\x08\x12\x15\n\rcan_subscribe\x18\x04 \x01(\x08\x12\x11\n\tschema_id\x18\x05 \x01(\t\x12\x0e\n\x06rpc_id\x18\x06 \x01(\t\"\"\n\x0cTopicRequest\x12\x12\n\ntopic_name\x18\x01 \x01(\t\")\n\x0b\x45ventHeader\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x0c\"j\n\rProducerEvent\x12\n\n\x02id\x18\x01 \x01(\t\x12\x11\n\tschema_id\x18\x02 \x01(\t\x12\x0f\n\x07payload\x18\x03 \x01(\x0c\x12)\n\x07headers\x18\x04 \x03(\x0b\x32\x18.eventbus.v1.EventHeader\"M\n\rConsumerEvent\x12)\n\x05\x65vent\x18\x01 \x01(\x0b\x32\x1a.eventbus.v1.ProducerEvent\x12\x11\n\treplay_id\x18\x02 \x01(\x0c\"^\n\rPublishResult\x12\x11\n\treplay_id\x18\x01 \x01(\x0c\x12!\n\x05\x65rror\x18\x02 \x01(\x0b\x32\x12.eventbus.v1.Error\x12\x17\n\x0f\x63orrelation_key\x18\x03 \x01(\t\":\n\x05\x45rror\x12$\n\x04\x63ode\x18\x01 \x01(\x0e\x32\x16.eventbus.v1.ErrorCode\x12\x0b\n\x03msg\x18\x02 \x01(\t\"\x94\x01\n\x0c\x46\x65tchRequest\x12\x12\n\ntopic_name\x18\x01 \x01(\t\x12\x30\n\rreplay_preset\x18\x02 \x01(\x0e\x32\x19.eventbus.v1.ReplayPreset\x12\x11\n\treplay_id\x18\x03 \x01(\x0c\x12\x15\n\rnum_requested\x18\x04 \x01(\x05\x12\x14\n\x0c\x61uth_refresh\x18\x05 \x01(\t\"\x84\x01\n\rFetchResponse\x12*\n\x06\x65vents\x18\x01 \x03(\x0b\x32\x1a.eventbus.v1.ConsumerEvent\x12\x18\n\x10latest_replay_id\x18\x02 \x01(\x0c\x12\x0e\n\x06rpc_id\x18\x03 \x01(\t\x12\x1d\n\x15pending_num_requested\x18\x04 \x01(\x05\"\"\n\rSchemaRequest\x12\x11\n\tschema_id\x18\x01 \x01(\t\"D\n\nSchemaInfo\x12\x13\n\x0bschema_json\x18\x01 \x01(\t\x12\x11\n\tschema_id\x18\x02 \x01(\t\x12\x0e\n\x06rpc_id\x18\x03 \x01(\t\"f\n\x0ePublishRequest\x12\x12\n\ntopic_name\x18\x01 \x01(\t\x12*\n\x06\x65vents\x18\x02 \x03(\x0b\x32\x1a.eventbus.v1.ProducerEvent\x12\x14\n\x0c\x61uth_refresh\x18\x03 \x01(\t\"a\n\x0fPublishResponse\x12+\n\x07results\x18\x01 \x03(\x0b\x32\x1a.eventbus.v1.PublishResult\x12\x11\n\tschema_id\x18\x02 \x01(\t\x12\x0e\n\x06rpc_id\x18\x03 \x01(\t\"\xb7\x01\n\x13ManagedFetchRequest\x12\x17\n\x0fsubscription_id\x18\x01 \x01(\t\x12\x16\n\x0e\x64\x65veloper_name\x18\x02 \x01(\t\x12\x15\n\rnum_requested\x18\x03 \x01(\x05\x12\x14\n\x0c\x61uth_refresh\x18\x04 \x01(\t\x12\x42\n\x18\x63ommit_replay_id_request\x18\x05 \x01(\x0b\x32 .eventbus.v1.CommitReplayRequest\"\xc7\x01\n\x14ManagedFetchResponse\x12*\n\x06\x65vents\x18\x01 \x03(\x0b\x32\x1a.eventbus.v1.ConsumerEvent\x12\x18\n\x10latest_replay_id\x18\x02 \x01(\x0c\x12\x0e\n\x06rpc_id\x18\x03 \x01(\t\x12\x1d\n\x15pending_num_requested\x18\x04 \x01(\x05\x12:\n\x0f\x63ommit_response\x18\x05 \x01(\x0b\x32!.eventbus.v1.CommitReplayResponse\"C\n\x13\x43ommitReplayRequest\x12\x19\n\x11\x63ommit_request_id\x18\x01 \x01(\t\x12\x11\n\treplay_id\x18\x02 \x01(\x0c\"}\n\x14\x43ommitReplayResponse\x12\x19\n\x11\x63ommit_request_id\x18\x01 \x01(\t\x12\x11\n\treplay_id\x18\x02 \x01(\x0c\x12!\n\x05\x65rror\x18\x03 \x01(\x0b\x32\x12.eventbus.v1.Error\x12\x14\n\x0cprocess_time\x18\x04 \x01(\x03*1\n\tErrorCode\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x0b\n\x07PUBLISH\x10\x01\x12\n\n\x06\x43OMMIT\x10\x02*4\n\x0cReplayPreset\x12\n\n\x06LATEST\x10\x00\x12\x0c\n\x08\x45\x41RLIEST\x10\x01\x12\n\n\x06\x43USTOM\x10\x02\x32\xc4\x03\n\x06PubSub\x12\x46\n\tSubscribe\x12\x19.eventbus.v1.FetchRequest\x1a\x1a.eventbus.v1.FetchResponse(\x01\x30\x01\x12@\n\tGetSchema\x12\x1a.eventbus.v1.SchemaRequest\x1a\x17.eventbus.v1.SchemaInfo\x12=\n\x08GetTopic\x12\x19.eventbus.v1.TopicRequest\x1a\x16.eventbus.v1.TopicInfo\x12\x44\n\x07Publish\x12\x1b.eventbus.v1.PublishRequest\x1a\x1c.eventbus.v1.PublishResponse\x12N\n\rPublishStream\x12\x1b.eventbus.v1.PublishRequest\x1a\x1c.eventbus.v1.PublishResponse(\x01\x30\x01\x12[\n\x10ManagedSubscribe\x12 .eventbus.v1.ManagedFetchRequest\x1a!.eventbus.v1.ManagedFetchResponse(\x01\x30\x01\x42\x61\n com.salesforce.eventbus.protobufB\x0bPubSubProtoP\x01Z.github.com/developerforce/pub-sub-api/go/protob\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'pubsub_api_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n com.salesforce.eventbus.protobufB\013PubSubProtoP\001Z.github.com/developerforce/pub-sub-api/go/proto'
  _globals['_ERRORCODE']._serialized_start=1768
  _globals['_ERRORCODE']._serialized_end=1817
  _globals['_REPLAYPRESET']._serialized_start=1819
  _globals['_REPLAYPRESET']._serialized_end=1871
  _globals['_TOPICINFO']._serialized_start=34
  _globals['_TOPICINFO']._serialized_end=165
  _globals['_TOPICREQUEST']._serialized_start=167
  _globals['_TOPICREQUEST']._serialized_end=201
  _globals['_EVENTHEADER']._serialized_start=203
  _globals['_EVENTHEADER']._serialized_end=244
  _globals['_PRODUCEREVENT']._serialized_start=246
  _globals['_PRODUCEREVENT']._serialized_end=352
  _globals['_CONSUMEREVENT']._serialized_start=354
  _globals['_CONSUMEREVENT']._serialized_end=431
  _globals['_PUBLISHRESULT']._serialized_start=433
  _globals['_PUBLISHRESULT']._serialized_end=527
  _globals['_ERROR']._serialized_start=529
  _globals['_ERROR']._serialized_end=587
  _globals['_FETCHREQUEST']._serialized_start=590
  _globals['_FETCHREQUEST']._serialized_end=738
  _globals['_FETCHRESPONSE']._serialized_start=741
  _globals['_FETCHRESPONSE']._serialized_end=873
  _globals['_SCHEMAREQUEST']._serialized_start=875
  _globals['_SCHEMAREQUEST']._serialized_end=909
  _globals['_SCHEMAINFO']._serialized_start=911
  _globals['_SCHEMAINFO']._serialized_end=979
  _globals['_PUBLISHREQUEST']._serialized_start=981
  _globals['_PUBLISHREQUEST']._serialized_end=1083
  _globals['_PUBLISHRESPONSE']._serialized_start=1085
  _globals['_PUBLISHRESPONSE']._serialized_end=1182
  _globals['_MANAGEDFETCHREQUEST']._serialized_start=1185
  _globals['_MANAGEDFETCHREQUEST']._serialized_end=1368
  _globals['_MANAGEDFETCHRESPONSE']._serialized_start=1371
  _globals['_MANAGEDFETCHRESPONSE']._serialized_end=1570
  _globals['_COMMITREPLAYREQUEST']._serialized_start=1572
  _globals['_COMMITREPLAYREQUEST']._serialized_end=1639
  _globals['_COMMITREPLAYRESPONSE']._serialized_start=1641
  _globals['_COMMITREPLAYRESPONSE']._serialized_end=1766
  _globals['_PUBSUB']._serialized_start=1874
  _globals['_PUBSUB']._serialized_end=2326
# @@protoc_insertion_point(module_scope)
