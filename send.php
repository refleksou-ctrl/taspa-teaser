<?php
// Join-the-team form: emails the entry to TO and sends the visitor back with a status.
// Nothing is stored; no third-party service. Needs PHP mail() (Zone.ee hosting has it).
const TO   = 'info@example.com';            // TODO: address that receives applications
const FROM = 'noreply@taspa.refleks.ee';    // must be a domain on this server

function back($hash) { header('Location: ./#' . $hash, true, 303); exit; }

if ($_SERVER['REQUEST_METHOD'] !== 'POST') back('tiim');
if (!empty($_POST['website'])) back('saadetud');          // honeypot: pretend success to bots

$clean = fn($k, $max) => trim(mb_substr((string)($_POST[$k] ?? ''), 0, $max));
$name = $clean('name', 100); $email = $clean('email', 150);
$phone = $clean('phone', 40); $msg = $clean('message', 3000);

if ($name === '' || $msg === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) back('viga');
$name = str_replace(["\r", "\n"], ' ', $name);             // no header injection via name

$body = "Nimi: $name\nE-post: $email\nTelefon: " . ($phone ?: '-') . "\n\n$msg\n";
$headers = "From: Taspa veeb <" . FROM . ">\r\nReply-To: $email\r\nContent-Type: text/plain; charset=UTF-8";
$subject = '=?UTF-8?B?' . base64_encode("Liitu TASPA tiimiga: $name") . '?=';

back(mail(TO, $subject, $body, $headers) ? 'saadetud' : 'viga');
