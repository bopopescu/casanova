require 'test_helper'

class AtletasControllerTest < ActionController::TestCase
  setup do
    @atleta = atletas(:one)
  end

  test "should get index" do
    get :index
    assert_response :success
    assert_not_nil assigns(:atletas)
  end

  test "should get new" do
    get :new
    assert_response :success
  end

  test "should create atleta" do
    assert_difference('Atleta.count') do
      post :create, :atleta => @atleta.attributes
    end

    assert_redirected_to atleta_path(assigns(:atleta))
  end

  test "should show atleta" do
    get :show, :id => @atleta.to_param
    assert_response :success
  end

  test "should get edit" do
    get :edit, :id => @atleta.to_param
    assert_response :success
  end

  test "should update atleta" do
    put :update, :id => @atleta.to_param, :atleta => @atleta.attributes
    assert_redirected_to atleta_path(assigns(:atleta))
  end

  test "should destroy atleta" do
    assert_difference('Atleta.count', -1) do
      delete :destroy, :id => @atleta.to_param
    end

    assert_redirected_to atletas_path
  end
end
