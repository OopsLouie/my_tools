#!/usr/bin/expect
set timeout -1


if {$argc < 5} {
    send_user "usage: $argv0 <source_file> <user_name> <target_ip_address> <target_file_path> <password>\n"
    exit
}

set source_file         [lindex $argv 0]
set user_name           [lindex $argv 1]
set target_ip_address   [lindex $argv 2]
set target_file_path    [lindex $argv 3]
set password            [lindex $argv 4]

spawn scp $source_file $user_name@$target_ip_address:$target_file_path
expect {
    "password" {send "$password\r";}
    "yes/no" {send "yes\r";exp_continue}
}
expect eof
exit
