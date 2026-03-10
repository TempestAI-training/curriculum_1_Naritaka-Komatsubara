/*⓪生徒の点数ごとにA〜Eのどの指標に分類されるかを表す関数(assignGrades)を定義する*/
const assignGrades = (scores) => {
    return scores.map((score) => {
        if(score >= 80){
        return "A"
        }else if(score >= 60){
        return "B"
        }else if(score >= 40){
        return "C"
        }else if(score >= 20){
        return "D"
        }else{
        return "E"
        }
    })
};

/*①生徒の人数を入力してもらう*/

const N = Number(window.prompt("生徒の人数を入力してください"));

/*②生徒の人数分の点数を一つずつ入力してもらう*/
/*③それらの点数で配列を作る*/

const testScores = [];

for(i = 1; i <= N; i++){
    console.log(i + '人目')
    const score = Number(window.prompt(i + "人目の生徒の点数を入力してください"))
    testScores.push(score)
};

console.log("入力された点数:", testScores);

/*④③の配列をassignGradesにいれ、結果をコンソールする*/

console.log("成績：", assignGrades(testScores));

/*フロー
⓪生徒の点数ごとにA〜Eのどの指標に分類されるかを表す関数(assignGrades)を定義する
①生徒の人数を入力してもらう
②生徒の人数分の点数を一つずつ入力してもらう
③それらの点数で配列を作る
④③の配列をassignGradesにいれ、結果をコンソールする
*/