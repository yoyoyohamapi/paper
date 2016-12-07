// 获得有效的服饰匹配,既包含上装又包含下装
db.yoho_items.aggregate([
    {
        $group: {
            _id: "$matching.id",
            categories: {$addToSet: "$category"}
        }
    },
    {
        $project: {size: {$size: "$categories"}}
    },
    {
        $match: {size: 2}
    },
    {
        $out: 'yoho_valid_matchings'
    }
]);
