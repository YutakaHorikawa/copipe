
var yamakiApp = angular.module('yamakiApp', []);

/**
 * Appの設定. httpリクエストヘッダーに追加情報
 * DjangoのCSRF対策に必要なtokenを渡す
 **/
yamakiApp.config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
});

/**
 * Appの設定
 * 変数スコープのブロック構造を変更。
 * デフォルトのままだとDjangoとかぶるため
 **/
yamakiApp.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});


/**
 * サーバーサイドにpostする処理をfactoryにまとめてみた
 **/
yamakiApp.factory('analyze', function($http) {
    var search = function(params) {
        //$.paramsが腑に落ちない
        return $http.post('/analysis/analyze/', $.param(params)).then(function(response) {
            return response.data;
        });
    };
    return {
        search: function(params) {
            return search(params);
        }
    };

});

/**
 * コントローラー
 **/
yamakiApp.controller('analysis', function ($scope, analyze) {
    
    // ボタンイベント
    $scope.sendData = function() {
        var params = {
            'v1': $scope.v1,
            'search_word': $scope.search_word,
            'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
        };

        analyze.search(params).then(function(data) {
            console.log(data.message);
            $scope.results = data.message;
        });

    };

});

