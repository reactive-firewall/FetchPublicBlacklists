require 'formula'

class FetchPublicBlacklists < Formula
  homepage 'https://github.com/reactive-firewall/FetchPublicBlacklists'
  url 'https://github.com/reactive-firewall/FetchPublicBlacklists/archive/master.zip'
  sha256 'e90c0379694be377962c5d9e28a2df6f2061ea241d756856ea9e697a95eec5df'
  version "0.3"

  depends_on 'python'

  def install
    system 'make', 'install'
  end
end