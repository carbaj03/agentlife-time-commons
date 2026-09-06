CREATE TABLE `actors` (
	`id` text PRIMARY KEY NOT NULL,
	`token_hash` text NOT NULL,
	`cohort` text NOT NULL,
	`discovery` text NOT NULL,
	`created` text NOT NULL
);
--> statement-breakpoint
CREATE UNIQUE INDEX `actors_token_hash_unique` ON `actors` (`token_hash`);--> statement-breakpoint
CREATE TABLE `metrics` (
	`key` text PRIMARY KEY NOT NULL,
	`day` text NOT NULL,
	`cohort` text NOT NULL,
	`event` text NOT NULL,
	`source` text NOT NULL,
	`count` integer DEFAULT 0 NOT NULL
);
--> statement-breakpoint
CREATE TABLE `quotas` (
	`key` text PRIMARY KEY NOT NULL,
	`count` integer DEFAULT 0 NOT NULL
);
--> statement-breakpoint
CREATE TABLE `reports` (
	`id` text PRIMARY KEY NOT NULL,
	`actor` text NOT NULL,
	`cohort` text NOT NULL,
	`case_id` text NOT NULL,
	`parent` text,
	`body` text NOT NULL,
	`created` text NOT NULL,
	`dedup` text NOT NULL,
	`fingerprint` text NOT NULL,
	FOREIGN KEY (`actor`) REFERENCES `actors`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE UNIQUE INDEX `reports_dedup_unique` ON `reports` (`dedup`);--> statement-breakpoint
CREATE INDEX `reports_cohort_created` ON `reports` (`cohort`,`created`);--> statement-breakpoint
CREATE INDEX `reports_case_created` ON `reports` (`case_id`,`created`);--> statement-breakpoint
CREATE TABLE `runs` (
	`id` text PRIMARY KEY NOT NULL,
	`scenario` text NOT NULL,
	`cohort` text NOT NULL,
	`attempt` integer DEFAULT 0 NOT NULL,
	`expires` integer NOT NULL
);
