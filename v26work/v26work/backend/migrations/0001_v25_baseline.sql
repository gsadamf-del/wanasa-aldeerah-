-- Wanasa V25 PostgreSQL baseline schema


CREATE TABLE audit_logs (
	id SERIAL NOT NULL, 
	actor_user_id INTEGER, 
	action VARCHAR(100) NOT NULL, 
	entity_type VARCHAR(100) NOT NULL, 
	entity_id INTEGER, 
	created_at TIMESTAMP WITHOUT TIME ZONE, 
	PRIMARY KEY (id)
);

CREATE TABLE banners (
	id SERIAL NOT NULL, 
	title VARCHAR(250) NOT NULL, 
	image_url VARCHAR(500), 
	link_url VARCHAR(500), 
	is_active BOOLEAN NOT NULL, 
	sort_order INTEGER NOT NULL, 
	PRIMARY KEY (id)
);

CREATE TABLE platform_settings (
	id SERIAL NOT NULL, 
	key VARCHAR(150) NOT NULL, 
	value TEXT, 
	PRIMARY KEY (id), 
	UNIQUE (key)
);

CREATE TABLE users (
	id SERIAL NOT NULL, 
	name VARCHAR(200) NOT NULL, 
	phone VARCHAR(50) NOT NULL, 
	password_hash VARCHAR(255) NOT NULL, 
	role VARCHAR(30) NOT NULL, 
	is_active BOOLEAN NOT NULL, 
	created_at TIMESTAMP WITHOUT TIME ZONE, 
	PRIMARY KEY (id), 
	UNIQUE (phone)
);

CREATE TABLE v19_device_tokens (
	id SERIAL NOT NULL, 
	user_id INTEGER NOT NULL, 
	token VARCHAR(512) NOT NULL, 
	platform VARCHAR(16) NOT NULL, 
	active BOOLEAN, 
	created_at TIMESTAMP WITHOUT TIME ZONE, 
	PRIMARY KEY (id), 
	UNIQUE (token)
);

CREATE TABLE v19_media_assets (
	id SERIAL NOT NULL, 
	owner_type VARCHAR(32) NOT NULL, 
	owner_id INTEGER NOT NULL, 
	url VARCHAR(1024) NOT NULL, 
	kind VARCHAR(32), 
	created_at TIMESTAMP WITHOUT TIME ZONE, 
	PRIMARY KEY (id)
);

CREATE TABLE v19_notifications (
	id SERIAL NOT NULL, 
	user_id INTEGER NOT NULL, 
	title VARCHAR(255) NOT NULL, 
	body VARCHAR(1000) NOT NULL, 
	event VARCHAR(64) NOT NULL, 
	read BOOLEAN, 
	created_at TIMESTAMP WITHOUT TIME ZONE, 
	PRIMARY KEY (id)
);

CREATE TABLE v19_payment_events (
	id SERIAL NOT NULL, 
	payment_id INTEGER NOT NULL, 
	event_type VARCHAR(64) NOT NULL, 
	payload VARCHAR, 
	created_at TIMESTAMP WITHOUT TIME ZONE, 
	PRIMARY KEY (id)
);

CREATE TABLE v19_payments (
	id SERIAL NOT NULL, 
	order_id INTEGER NOT NULL, 
	amount FLOAT NOT NULL, 
	currency VARCHAR(8), 
	provider VARCHAR(64) NOT NULL, 
	status VARCHAR(32), 
	reference VARCHAR(128), 
	created_at TIMESTAMP WITHOUT TIME ZONE, 
	PRIMARY KEY (id)
);

CREATE TABLE v20_idempotency_keys (
	id SERIAL NOT NULL, 
	user_id INTEGER NOT NULL, 
	key VARCHAR(128) NOT NULL, 
	endpoint VARCHAR(160) NOT NULL, 
	response_json TEXT NOT NULL, 
	status_code INTEGER NOT NULL, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_v20_idempotency UNIQUE (user_id, key, endpoint)
);

CREATE TABLE v20_payment_webhooks (
	id SERIAL NOT NULL, 
	provider VARCHAR(64) NOT NULL, 
	event_id VARCHAR(128) NOT NULL, 
	signature_valid BOOLEAN NOT NULL, 
	payload TEXT NOT NULL, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (event_id)
);

CREATE TABLE v21_audit_events (
	id SERIAL NOT NULL, 
	actor_user_id INTEGER, 
	action VARCHAR(100) NOT NULL, 
	entity_type VARCHAR(100) NOT NULL, 
	entity_id INTEGER, 
	request_id VARCHAR(64), 
	ip_address VARCHAR(64), 
	metadata_json TEXT, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id)
);

CREATE TABLE v21_outbox_events (
	id SERIAL NOT NULL, 
	event_id VARCHAR(128) NOT NULL, 
	topic VARCHAR(128) NOT NULL, 
	aggregate_type VARCHAR(100) NOT NULL, 
	aggregate_id INTEGER, 
	payload_json TEXT NOT NULL, 
	status VARCHAR(24) NOT NULL, 
	attempts INTEGER NOT NULL, 
	available_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	processed_at TIMESTAMP WITHOUT TIME ZONE, 
	last_error TEXT, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (event_id)
);

CREATE TABLE v21_reconciliation_runs (
	id SERIAL NOT NULL, 
	run_key VARCHAR(128) NOT NULL, 
	scope VARCHAR(64) NOT NULL, 
	status VARCHAR(24) NOT NULL, 
	checked_count INTEGER NOT NULL, 
	mismatch_count INTEGER NOT NULL, 
	summary_json TEXT NOT NULL, 
	started_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	finished_at TIMESTAMP WITHOUT TIME ZONE, 
	PRIMARY KEY (id), 
	UNIQUE (run_key)
);

CREATE TABLE v21_security_events (
	id SERIAL NOT NULL, 
	event_type VARCHAR(100) NOT NULL, 
	severity VARCHAR(16) NOT NULL, 
	actor_user_id INTEGER, 
	request_id VARCHAR(64), 
	detail TEXT, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id)
);

CREATE TABLE v22_backup_drills (
	id SERIAL NOT NULL, 
	drill_key VARCHAR(128) NOT NULL, 
	status VARCHAR(24) NOT NULL, 
	verified_at TIMESTAMP WITHOUT TIME ZONE, 
	notes TEXT, 
	PRIMARY KEY (id), 
	UNIQUE (drill_key)
);

CREATE TABLE v22_dead_letter_events (
	id SERIAL NOT NULL, 
	source_event_id VARCHAR(128) NOT NULL, 
	topic VARCHAR(128) NOT NULL, 
	payload_json TEXT NOT NULL, 
	attempts INTEGER NOT NULL, 
	error TEXT, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	resolved BOOLEAN NOT NULL, 
	PRIMARY KEY (id)
);

CREATE TABLE v22_metric_samples (
	id SERIAL NOT NULL, 
	metric VARCHAR(100) NOT NULL, 
	value INTEGER NOT NULL, 
	bucket VARCHAR(64) NOT NULL, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_v22_metric_bucket UNIQUE (metric, bucket)
);

CREATE TABLE v22_rate_limit_buckets (
	id SERIAL NOT NULL, 
	bucket_key VARCHAR(255) NOT NULL, 
	window_started_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	request_count INTEGER NOT NULL, 
	updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (bucket_key)
);

CREATE TABLE v23_operational_incidents (
	id SERIAL NOT NULL, 
	incident_key VARCHAR(128) NOT NULL, 
	severity VARCHAR(32) NOT NULL, 
	status VARCHAR(32) NOT NULL, 
	detail TEXT, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	resolved BOOLEAN NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (incident_key)
);

CREATE TABLE v23_worker_heartbeats (
	id SERIAL NOT NULL, 
	worker_name VARCHAR(128) NOT NULL, 
	status VARCHAR(32) NOT NULL, 
	last_seen_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	detail TEXT, 
	PRIMARY KEY (id), 
	UNIQUE (worker_name)
);

CREATE TABLE v24_migration_preflights (
	id SERIAL NOT NULL, 
	run_key VARCHAR(128) NOT NULL, 
	status VARCHAR(24) NOT NULL, 
	checked_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	detail TEXT, 
	passed BOOLEAN NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (run_key)
);

CREATE TABLE v24_schema_migrations (
	id SERIAL NOT NULL, 
	revision VARCHAR(64) NOT NULL, 
	applied_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	checksum VARCHAR(128) NOT NULL, 
	notes TEXT, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_v24_schema_revision UNIQUE (revision), 
	UNIQUE (revision)
);

CREATE TABLE v25_external_provider_health (
	id SERIAL NOT NULL, 
	provider VARCHAR(64) NOT NULL, 
	status VARCHAR(24) NOT NULL, 
	latency_ms FLOAT, 
	checked_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	detail TEXT, 
	PRIMARY KEY (id), 
	UNIQUE (provider)
);

CREATE TABLE v25_monitoring_events (
	id SERIAL NOT NULL, 
	event_type VARCHAR(64) NOT NULL, 
	severity VARCHAR(24) NOT NULL, 
	message TEXT NOT NULL, 
	external_id VARCHAR(128), 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id)
);

CREATE TABLE v25_restore_drills (
	id SERIAL NOT NULL, 
	drill_key VARCHAR(128) NOT NULL, 
	source_backup VARCHAR(512) NOT NULL, 
	target_database VARCHAR(256) NOT NULL, 
	status VARCHAR(32) NOT NULL, 
	started_at TIMESTAMP WITHOUT TIME ZONE, 
	completed_at TIMESTAMP WITHOUT TIME ZONE, 
	verified BOOLEAN NOT NULL, 
	notes TEXT, 
	PRIMARY KEY (id), 
	UNIQUE (drill_key)
);

CREATE TABLE merchants (
	id SERIAL NOT NULL, 
	user_id INTEGER, 
	name VARCHAR(200) NOT NULL, 
	status VARCHAR(30) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE orders (
	id SERIAL NOT NULL, 
	customer_id INTEGER NOT NULL, 
	status VARCHAR(40) NOT NULL, 
	subtotal NUMERIC(12, 2) NOT NULL, 
	vat NUMERIC(12, 2) NOT NULL, 
	delivery_fee NUMERIC(12, 2) NOT NULL, 
	total NUMERIC(12, 2) NOT NULL, 
	created_at TIMESTAMP WITHOUT TIME ZONE, 
	PRIMARY KEY (id), 
	FOREIGN KEY(customer_id) REFERENCES users (id)
);

CREATE TABLE products (
	id SERIAL NOT NULL, 
	merchant_id INTEGER, 
	name VARCHAR(250) NOT NULL, 
	category VARCHAR(100), 
	description TEXT, 
	price NUMERIC(12, 2) NOT NULL, 
	stock INTEGER NOT NULL, 
	expiry_date DATE, 
	is_active BOOLEAN NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(merchant_id) REFERENCES merchants (id)
);

CREATE TABLE v20_delivery_locations (
	id SERIAL NOT NULL, 
	order_id INTEGER NOT NULL, 
	courier_user_id INTEGER NOT NULL, 
	latitude NUMERIC(10, 7) NOT NULL, 
	longitude NUMERIC(10, 7) NOT NULL, 
	recorded_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(order_id) REFERENCES orders (id)
);

CREATE TABLE v20_settlement_entries (
	id SERIAL NOT NULL, 
	merchant_id INTEGER NOT NULL, 
	order_id INTEGER, 
	gross_amount NUMERIC(12, 2) NOT NULL, 
	commission_amount NUMERIC(12, 2) NOT NULL, 
	net_amount NUMERIC(12, 2) NOT NULL, 
	status VARCHAR(24) NOT NULL, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(order_id) REFERENCES orders (id)
);

CREATE TABLE offers (
	id SERIAL NOT NULL, 
	product_id INTEGER NOT NULL, 
	title VARCHAR(250) NOT NULL, 
	discount_percent NUMERIC(5, 2) NOT NULL, 
	start_at TIMESTAMP WITHOUT TIME ZONE, 
	end_at TIMESTAMP WITHOUT TIME ZONE, 
	is_active BOOLEAN NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(product_id) REFERENCES products (id)
);

CREATE TABLE order_items (
	id SERIAL NOT NULL, 
	order_id INTEGER NOT NULL, 
	product_id INTEGER NOT NULL, 
	quantity INTEGER NOT NULL, 
	unit_price NUMERIC(12, 2) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(order_id) REFERENCES orders (id), 
	FOREIGN KEY(product_id) REFERENCES products (id)
);

CREATE TABLE v20_inventory_events (
	id SERIAL NOT NULL, 
	product_id INTEGER NOT NULL, 
	order_id INTEGER, 
	event_type VARCHAR(32) NOT NULL, 
	quantity INTEGER NOT NULL, 
	balance_after INTEGER NOT NULL, 
	idempotency_key VARCHAR(128), 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(product_id) REFERENCES products (id), 
	FOREIGN KEY(order_id) REFERENCES orders (id), 
	UNIQUE (idempotency_key)
);

CREATE INDEX ix_v19_device_tokens_user_id ON v19_device_tokens (user_id);

CREATE INDEX ix_v19_media_assets_owner_id ON v19_media_assets (owner_id);

CREATE INDEX ix_v19_notifications_user_id ON v19_notifications (user_id);

CREATE INDEX ix_v19_payment_events_payment_id ON v19_payment_events (payment_id);

CREATE INDEX ix_v19_payments_order_id ON v19_payments (order_id);

CREATE INDEX ix_v20_idempotency_keys_user_id ON v20_idempotency_keys (user_id);

CREATE INDEX ix_v21_audit_events_actor_user_id ON v21_audit_events (actor_user_id);

CREATE INDEX ix_v21_audit_events_entity_id ON v21_audit_events (entity_id);

CREATE INDEX ix_v21_audit_events_created_at ON v21_audit_events (created_at);

CREATE INDEX ix_v21_audit_events_request_id ON v21_audit_events (request_id);

CREATE INDEX ix_v21_outbox_events_available_at ON v21_outbox_events (available_at);

CREATE INDEX ix_v21_outbox_events_aggregate_id ON v21_outbox_events (aggregate_id);

CREATE INDEX ix_v21_outbox_pending ON v21_outbox_events (status, available_at);

CREATE INDEX ix_v21_outbox_events_status ON v21_outbox_events (status);

CREATE INDEX ix_v21_outbox_events_topic ON v21_outbox_events (topic);

CREATE INDEX ix_v21_security_events_request_id ON v21_security_events (request_id);

CREATE INDEX ix_v21_security_events_event_type ON v21_security_events (event_type);

CREATE INDEX ix_v21_security_events_created_at ON v21_security_events (created_at);

CREATE INDEX ix_v21_security_events_actor_user_id ON v21_security_events (actor_user_id);

CREATE INDEX ix_v22_dead_letter_events_source_event_id ON v22_dead_letter_events (source_event_id);

CREATE INDEX ix_v22_dead_letter_events_resolved ON v22_dead_letter_events (resolved);

CREATE INDEX ix_v22_dead_letter_events_topic ON v22_dead_letter_events (topic);

CREATE INDEX ix_v22_dead_letter_events_created_at ON v22_dead_letter_events (created_at);

CREATE INDEX ix_v22_metric_samples_metric ON v22_metric_samples (metric);

CREATE INDEX ix_v22_metric_samples_bucket ON v22_metric_samples (bucket);

CREATE INDEX ix_v22_metric_samples_created_at ON v22_metric_samples (created_at);

CREATE INDEX ix_v20_delivery_locations_courier_user_id ON v20_delivery_locations (courier_user_id);

CREATE INDEX ix_v20_delivery_locations_order_id ON v20_delivery_locations (order_id);

CREATE INDEX ix_v20_settlement_entries_merchant_id ON v20_settlement_entries (merchant_id);

CREATE INDEX ix_v20_inventory_events_order_id ON v20_inventory_events (order_id);

CREATE INDEX ix_v20_inventory_events_product_id ON v20_inventory_events (product_id);
