.class public Lcom/u8/sdk/SplashActivity;
.super Landroid/app/Activity;
.source "SplashActivity.java"


# direct methods
.method public constructor <init>()V
    .locals 0

    invoke-direct {p0}, Landroid/app/Activity;-><init>()V

    return-void
.end method

.method static synthetic access$0(Lcom/u8/sdk/SplashActivity;)V
    .locals 0

    invoke-direct {p0}, Lcom/u8/sdk/SplashActivity;->startGameActivity()V

    return-void
.end method

.method private appendAnimation()V
    .locals 9

    const/4 v8, 0x0

    new-instance v0, Landroid/view/animation/AlphaAnimation;

    const/4 v4, 0x0

    const/high16 v5, 0x3f800000

    invoke-direct {v0, v4, v5}, Landroid/view/animation/AlphaAnimation;-><init>(FF)V

    const/4 v4, 0x2

    invoke-virtual {v0, v4}, Landroid/view/animation/AlphaAnimation;->setRepeatMode(I)V

    invoke-virtual {v0, v8}, Landroid/view/animation/AlphaAnimation;->setRepeatCount(I)V

    const-wide/16 v4, 0x7d0

    invoke-virtual {v0, v4, v5}, Landroid/view/animation/AlphaAnimation;->setDuration(J)V

    invoke-virtual {p0}, Lcom/u8/sdk/SplashActivity;->getResources()Landroid/content/res/Resources;

    move-result-object v4

    const-string v5, "u8_splash_img"

    const-string v6, "id"

    invoke-virtual {p0}, Lcom/u8/sdk/SplashActivity;->getPackageName()Ljava/lang/String;

    move-result-object v7

    invoke-virtual {v4, v5, v6, v7}, Landroid/content/res/Resources;->getIdentifier(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)I

    move-result v4

    invoke-virtual {p0, v4}, Lcom/u8/sdk/SplashActivity;->findViewById(I)Landroid/view/View;

    move-result-object v2

    check-cast v2, Landroid/widget/ImageView;

    if-nez v2, :cond_0

    invoke-virtual {p0}, Lcom/u8/sdk/SplashActivity;->getResources()Landroid/content/res/Resources;

    move-result-object v4

    const-string v5, "u8_splash_layout"

    const-string v6, "id"

    invoke-virtual {p0}, Lcom/u8/sdk/SplashActivity;->getPackageName()Ljava/lang/String;

    move-result-object v7

    invoke-virtual {v4, v5, v6, v7}, Landroid/content/res/Resources;->getIdentifier(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)I

    move-result v1

    invoke-static {p0}, Landroid/view/LayoutInflater;->from(Landroid/content/Context;)Landroid/view/LayoutInflater;

    move-result-object v4

    const/4 v5, 0x0

    invoke-virtual {v4, v1, v5}, Landroid/view/LayoutInflater;->inflate(ILandroid/view/ViewGroup;)Landroid/view/View;

    move-result-object v3

    check-cast v3, Landroid/widget/RelativeLayout;

    invoke-virtual {v3, v8}, Landroid/widget/RelativeLayout;->getChildAt(I)Landroid/view/View;

    move-result-object v2

    check-cast v2, Landroid/widget/ImageView;

    :cond_0
    invoke-virtual {v2, v0}, Landroid/widget/ImageView;->setAnimation(Landroid/view/animation/Animation;)V

    new-instance v4, Lcom/u8/sdk/SplashActivity$1;

    invoke-direct {v4, p0}, Lcom/u8/sdk/SplashActivity$1;-><init>(Lcom/u8/sdk/SplashActivity;)V

    invoke-virtual {v0, v4}, Landroid/view/animation/AlphaAnimation;->setAnimationListener(Landroid/view/animation/Animation$AnimationListener;)V

    return-void
.end method

.method private startGameActivity()V
    .locals 4

    :try_start_0
    const-string v3, "{U8SDK_Game_Activity}"

    invoke-static {v3}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v2

    new-instance v1, Landroid/content/Intent;

    invoke-direct {v1, p0, v2}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    invoke-virtual {p0, v1}, Lcom/u8/sdk/SplashActivity;->startActivity(Landroid/content/Intent;)V

    invoke-virtual {p0}, Lcom/u8/sdk/SplashActivity;->finish()V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    :goto_0
    return-void

    :catch_0
    move-exception v0

    invoke-virtual {v0}, Ljava/lang/Exception;->printStackTrace()V

    goto :goto_0
.end method


# virtual methods
.method public onCreate(Landroid/os/Bundle;)V
    .locals 5
    .param p1    # Landroid/os/Bundle;

    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V

    invoke-virtual {p0}, Lcom/u8/sdk/SplashActivity;->getResources()Landroid/content/res/Resources;

    move-result-object v1

    const-string v2, "u8_splash"

    const-string v3, "layout"

    invoke-virtual {p0}, Lcom/u8/sdk/SplashActivity;->getPackageName()Ljava/lang/String;

    move-result-object v4

    invoke-virtual {v1, v2, v3, v4}, Landroid/content/res/Resources;->getIdentifier(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)I

    move-result v0

    invoke-virtual {p0, v0}, Lcom/u8/sdk/SplashActivity;->setContentView(I)V

    invoke-direct {p0}, Lcom/u8/sdk/SplashActivity;->appendAnimation()V

    return-void
.end method
