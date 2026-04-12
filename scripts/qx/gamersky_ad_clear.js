// Gamersky ad clear script for Quantumult X
// Created: 2025-06-20
// This script clears ad configurations from Gamersky app

var body = $response.body;
var obj = JSON.parse(body);

// Clear ad configurations
if (obj.config) {
  // Clear ad IDs and related configurations
  if (obj.config.androidLaunchAdIdSIGMOB) obj.config.androidLaunchAdIdSIGMOB = "";
  if (obj.config.androidListAdIdSIGMOB) obj.config.androidListAdIdSIGMOB = "";
  if (obj.config.androidLaunchAdIdUBIX) obj.config.androidLaunchAdIdUBIX = "";
  if (obj.config.androidListAdIdUBIX) obj.config.androidListAdIdUBIX = "";
  if (obj.config.androidLaunchAdIdBeiZi) obj.config.androidLaunchAdIdBeiZi = "";
  if (obj.config.androidListAdIdAdTroop) obj.config.androidListAdIdAdTroop = "";
  if (obj.config.androidLaunchAdIdChuanShanJia) obj.config.androidLaunchAdIdChuanShanJia = "";
  if (obj.config.androidListAdIdChuanShanJia) obj.config.androidListAdIdChuanShanJia = "";
  if (obj.config.androidListAdIdTapADN) obj.config.androidListAdIdTapADN = "";
  if (obj.config.androidPostPageRelatedAdId) obj.config.androidPostPageRelatedAdId = "";
  if (obj.config.androidPostPageBottomAdId) obj.config.androidPostPageBottomAdId = "";
  
  // iOS ad configurations
  if (obj.config.ioslaunchAdIdUBIX) obj.config.ioslaunchAdIdUBIX = "";
  if (obj.config.ioslistAdIdUBIX) obj.config.ioslistAdIdUBIX = "";
  if (obj.config.ioslaunchAdIdWhalessp) obj.config.ioslaunchAdIdWhalessp = "";
  if (obj.config.ioslaunchAdIdChuanShanJia) obj.config.ioslaunchAdIdChuanShanJia = "";
  if (obj.config.ioslistAdIdChuanShanJia) obj.config.ioslistAdIdChuanShanJia = "";
  if (obj.config.ioslaunchAdIdGuangDianTong) obj.config.ioslaunchAdIdGuangDianTong = "";
  if (obj.config.ioslaunchAdIdAdTroop) obj.config.ioslaunchAdIdAdTroop = "";
  if (obj.config.ioslistAdIdAdTroop) obj.config.ioslistAdIdAdTroop = "";
  if (obj.config.iosPostPageBottomAdId) obj.config.iosPostPageBottomAdId = "";
  
  // Set ad percentages to 0
  if (obj.config.androidLaunchAdPercentageSIGMOB) obj.config.androidLaunchAdPercentageSIGMOB = 0;
  if (obj.config.androidLaunchAdPercentageUBIX) obj.config.androidLaunchAdPercentageUBIX = 0;
  if (obj.config.androidLaunchAdPercentageBeiZi) obj.config.androidLaunchAdPercentageBeiZi = 0;
  if (obj.config.androidListAdPercentageSIGMOB) obj.config.androidListAdPercentageSIGMOB = 0;
  if (obj.config.androidListAdPercentageUBIX) obj.config.androidListAdPercentageUBIX = 0;
  if (obj.config.androidListAdPercentageTapADN) obj.config.androidListAdPercentageTapADN = 0;
  if (obj.config.ioslaunchAdPercentageUBIX) obj.config.ioslaunchAdPercentageUBIX = 0;
  if (obj.config.ioslaunchAdPercentageWhalessp) obj.config.ioslaunchAdPercentageWhalessp = 0;
  if (obj.config.ioslaunchAdPercentageAdTroop) obj.config.ioslaunchAdPercentageAdTroop = 0;
  if (obj.config.ioslistAdPercentageUBIX) obj.config.ioslistAdPercentageUBIX = 0;
  if (obj.config.ioslistAdPercentageADTroop) obj.config.ioslistAdPercentageADTroop = 0;
  
  // Disable ad providers
  if (obj.config.androidLaunchAdProviderName) obj.config.androidLaunchAdProviderName = "close";
  if (obj.config.androidListWangMengAdProviderName) obj.config.androidListWangMengAdProviderName = "close";
  if (obj.config.androidListZhiKeAdProviderName) obj.config.androidListZhiKeAdProviderName = "close";
  if (obj.config.ioslaunchAdProviderName) obj.config.ioslaunchAdProviderName = "close";
  if (obj.config.ioslistWangMengAdProviderName) obj.config.ioslistWangMengAdProviderName = "close";
  if (obj.config.ioslistZhiKeAdProviderName) obj.config.ioslistZhiKeAdProviderName = "close";
  
  // Disable ad display settings
  if (obj.config.androidLaunchAdFullDisplay) obj.config.androidLaunchAdFullDisplay = false;
  if (obj.config.iosLaunchAdFullDisplay) obj.config.iosLaunchAdFullDisplay = false;
  if (obj.config.androidPostPageRelatedAdProvider) obj.config.androidPostPageRelatedAdProvider = "close";
  if (obj.config.androidPostPageBottomAdProvider) obj.config.androidPostPageBottomAdProvider = "close";
  if (obj.config.iosPostPageRelatedAdProvider) obj.config.iosPostPageRelatedAdProvider = "close";
  if (obj.config.iosPostPageBottomAdProvider) obj.config.iosPostPageBottomAdProvider = "close";
  
  // Set ad display intervals to maximum
  if (obj.config.androidLaunchAdShowIntervalSeconds) obj.config.androidLaunchAdShowIntervalSeconds = 999999999;
  if (obj.config.ioslaunchAdShowIntervalSeconds) obj.config.ioslaunchAdShowIntervalSeconds = 999999999;
}

$done({body: JSON.stringify(obj)});