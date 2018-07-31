.class Lcom/u8/sdk/SplashActivity$1;
.super Ljava/lang/Object;
.source "SplashActivity.java"

# interfaces
.implements Landroid/view/animation/Animation$AnimationListener;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/u8/sdk/SplashActivity;->appendAnimation()V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/u8/sdk/SplashActivity;


# direct methods
.method constructor <init>(Lcom/u8/sdk/SplashActivity;)V
    .locals 0

    iput-object p1, p0, Lcom/u8/sdk/SplashActivity$1;->this$0:Lcom/u8/sdk/SplashActivity;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public onAnimationEnd(Landroid/view/animation/Animation;)V
    .locals 1
    .param p1    # Landroid/view/animation/Animation;

    iget-object v0, p0, Lcom/u8/sdk/SplashActivity$1;->this$0:Lcom/u8/sdk/SplashActivity;

    # invokes: Lcom/u8/sdk/SplashActivity;->startGameActivity()V
    invoke-static {v0}, Lcom/u8/sdk/SplashActivity;->access$0(Lcom/u8/sdk/SplashActivity;)V

    return-void
.end method

.method public onAnimationRepeat(Landroid/view/animation/Animation;)V
    .locals 0
    .param p1    # Landroid/view/animation/Animation;

    return-void
.end method

.method public onAnimationStart(Landroid/view/animation/Animation;)V
    .locals 0
    .param p1    # Landroid/view/animation/Animation;

    return-void
.end method
