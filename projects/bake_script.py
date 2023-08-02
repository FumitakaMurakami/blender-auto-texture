import bpy
import time

class ObjectSupport:
    '''
    オブジェクトの処理をするクラス
    '''
    # オブジェクト削除
    def delete_target_object(self, object_name):
        target_obj = bpy.data.objects.get(object_name)

        # 指定オブジェクトが存在するか確認する
        if target_obj != None:
            # オブジェクトが存在する場合は削除を行う
            bpy.data.objects.remove(target_obj)

    # 追加オブジェクトキー取得
    def get_add_object_name(self):
        names = []
        # 初期オブジェクト以外のオブジェクトキー取得
        for key in bpy.data.objects.keys():
            if key != 'Camera' and key != 'Light':
                names.append(key)
        return names

    # 指定オブジェクトに指定の画像テクスチャを設定したプリンシプルBSDFのマテリアルを設定する
    def set_object_texture(self, target_object, texture_path):
        #TextureSupportクラスのインスタンス取得
        tex_sup = TextureSupport()

        # 指定オブジェクトの全マテリアルを削除する
        delmat_result = tex_sup.delete_material_all(target_object)

        # マテリアル名を設定する
        make_materialname = "TextureMaterial"

        # 作成マテリアルにプリンシプルBSDFノードを追加して画像ノードをカラーとして接続する
        new_result = tex_sup.new_bsdfmaterial_texture(arg_materialname=make_materialname, texture_path=texture_path)

        # 作成マテリアルをセットする
        set_result = tex_sup.add_material_target(target_object, arg_materialname=make_materialname)

class BakeObject:
    '''
    テクスチャのベイク処理に関するクラス
    '''

    # ベイク設定
    def bake_setting(self):
        # レンダリングエンジンを CYCLES に切り替える
        bpy.context.scene.render.engine = 'CYCLES'

        # GPUの利用有無を確認する
        GPUuse=True
        if GPUuse == True:
            # 利用設定ならGPUの設定を行う
            bpy.data.scenes["Scene"].cycles.device = 'GPU'

        # render.bake の設定項目を予め設定する
        bake_setting = bpy.context.scene.render.bake

        # 直接照明の影響設定
        bake_setting.use_pass_direct = True

        # 間接照明の影響設定
        bake_setting.use_pass_indirect = False

        # カラーの影響設定
        bake_setting.use_pass_color = True

    # テクスチャ画像設定
    def bake_texture_setting(self, target_object, texturenode_name, bake_image):

        # 参照の保存用変数
        name_mapping = {}

        # TextureSupportクラスインスタンス取得
        tex_sup = TextureSupport()

        # 指定オブジェクトのマテリアルリストを取得する
        for material_slot in target_object.material_slots:
            # スロットのマテリアルを取得する
            target_material = material_slot.material

            # マテリアルが割り当てられているか
            if target_material == None:
                continue

            # 参照マテリアルをノード使用に変更する
            tex_sup.use_material_node(target_material)

            # 新規テクスチャを参照する画像ノードを追加する
            add_node = tex_sup.add_node_image(
                material=target_material,
                image=bake_image
            )

            # 作成ノードの参照を保存する
            name_mapping[texturenode_name + target_material.name] = add_node

            # 指定の画像ノードを選択状態に設定する
            tex_sup.select_node_target(
                material=target_material,
                node=name_mapping[texturenode_name + target_material.name]
            )
    
        return name_mapping

    def bake_object(self, bake_type, save_mode):
        # ベイクの実行
        bpy.ops.object.bake(type=bake_type, save_mode=save_mode)


class TextureSupport:
    '''
    テクスチャに関するクラス
    テクスチャの貼り付けやマテリアル、ノード操作に関する処理を記載する
    '''

    # 指定テクスチャを設定したプリンシプルBSDFマテリアルを作成する
    def new_bsdfmaterial_texture(self, arg_materialname="TextureMaterial", texture_path=""):

        # 指定名のマテリアルを取得する
        check_mat = bpy.data.materials.get(arg_materialname)

        # 指定名のマテリアルが存在するか確認する
        if check_mat != None:
            # 指定名のマテリアルが既に存在する場合は処理しない
            return False

        # 新規マテリアルを作成する
        newmaterial = bpy.data.materials.new(arg_materialname)

        # ノードを使用する
        newmaterial.use_nodes = True

        # 処理対象のマテリアルを取得する
        target_mat = newmaterial

        # ターゲットマテリアルのノード参照を取得
        mat_nodes = target_mat.node_tree.nodes

        # マテリアル内の全ノードを走査する
        for delete_node in mat_nodes:
            # 一旦デフォルトのノードを全て削除する
            mat_nodes.remove(delete_node)
    
        # テクスチャノードの追加
        texture_node = mat_nodes.new(type="ShaderNodeTexImage")

        # テクスチャノードをアクティブにする
        mat_nodes.active = texture_node

        # 指定画像を読み込む
        loadimage = bpy.data.images.load(filepath=texture_path)

        # テクスチャノードに新規画像を設定する
        texture_node.image = loadimage

        # ノードリンクの取得
        mat_link = target_mat.node_tree.links

        # プリンシプルBSDFノードを追加する
        bsdf_node = mat_nodes.new(type="ShaderNodeBsdfPrincipled")

        # 出力ノードを追加する
        output_node = mat_nodes.new(type="ShaderNodeOutputMaterial")

        # テクスチャノードのカラーとプリンシプルBSDFノードのベースカラーを接続する
        mat_link.new(texture_node.outputs[0], bsdf_node.inputs[0])

        # 放射ノードの放射と出力ノードのサーフェスを接続する
        mat_link.new(bsdf_node.outputs[0], output_node.inputs[0])

    # 指定オブジェクトに指定名のマテリアルを追加する
    def add_material_target(self, target_object,
        arg_materialname="NewMaterial", arg_usenode=True):

        # オブジェクトをアクティブにする
        bpy.context.view_layer.objects.active = target_object

        # 指定名のマテリアルを取得する
        add_mat = bpy.data.materials.get(arg_materialname)

        # 指定名のマテリアルが存在するか確認する
        if add_mat == None:
            # 指定名のマテリアルが存在しない場合は新規マテリアルを作成する
            add_mat = bpy.data.materials.new(arg_materialname)

            # ノードの利用指定を確認する
            if arg_usenode == True:
                # ノードを使用する
                add_mat.use_nodes = True

        # 指定名のマテリアルスロットを取得する
        check_matslot = target_object.material_slots.get(arg_materialname)

        # 指定マテリアルが存在するか確認する
        if check_matslot != None:
            # 指定名のマテリアルスロットが既に存在する場合は処理しない
            return False

        # マテリアルスロットを追加する
        bpy.ops.object.material_slot_add()

        # 追加したマテリアルスロットに指定名のマテリアルを設定する
        target_object.active_material = add_mat

    # 指定オブジェクトの全マテリアルを削除する
    def delete_material_all(self, target_object):

        # マテリアルスロットを走査する
        for material_slot in target_object.material_slots:

            # マテリアルスロットをアクティブにする
            target_object.active_material = material_slot.material

            # マテリアルスロットを削除する
            bpy.ops.object.material_slot_remove()

    # 対象マテリアルのノードを有効化する
    def use_material_node(self, material):

        # ノードが無効な場合、有効化する
        if material.use_nodes == False:
            material.use_nodes = True

        return

    # 対象マテリアルの指定ノードのみを選択状態する
    def select_node_target(self, material:bpy.types.Material, node:bpy.types.Node):

        # ターゲットマテリアルのノード参照を取得
        mat_nodes = material.node_tree.nodes

        # 全てのノードの選択状態を解除する
        for mat_node in mat_nodes:
            # 選択状態を解除する
            mat_node.select = False

        # 指定ノードを選択状態にする
        node.select = True

        # 指定ノードをアクティブにする
        mat_nodes.active = node
    
    # 対象マテリアルの指定ノードを削除する
    def delete_node_target(self, material:bpy.types.Material, node:bpy.types.Node):

        # ターゲットマテリアルのノード参照を取得
        mat_nodes = material.node_tree.nodes

        # ノードを削除する
        mat_nodes.remove(node)

        return

    # 対象マテリアルに指定テクスチャを参照する画像ノードを追加する
    def add_node_image(self, material:bpy.types.Material,
        image:bpy.types.Image) -> bpy.types.Node:

        # ターゲットマテリアルのノード参照を取得
        mat_nodes = material.node_tree.nodes

        # テクスチャノードの追加
        texture_node = mat_nodes.new(type="ShaderNodeTexImage")

        # テクスチャノードに指定画像を設定する
        texture_node.image = image

        return texture_node

    # 新規画像を作成する
    def make_new_image(self, texturename, texturesize) -> bpy.types.Image:

        # 新規画像を作成する
        newimage = bpy.data.images.new(
            name=texturename,
            width=texturesize,
            height=texturesize,
            alpha=True
        )

        return newimage

# オブジェクトのベイク
def create_bake_texture(obj, texture_path, bake_obj=BakeObject(), tex_sup=TextureSupport()):
    '''
    オブジェクトをベイクしてテクスチャを生成し、PNGとして保存するメソッド
    '''
    texturenode_name = "ForBakeTextureNode"

    # 新規テクスチャを作成して参照を取得する
    bake_image = tex_sup.make_new_image(
        texturename="BakeTexture",
        texturesize=2048
    )

    # 追加オブジェクトを選択状態にする
    obj.select_set(True)

    # 指定オブジェクトをアクティブにする
    bpy.context.view_layer.objects.active = obj

    # ベイクするオブジェクトのテクスチャの設定
    name_mapping = bake_obj.bake_texture_setting(obj, texturenode_name, bake_image)

    # ベイクの設定
    bake_obj.bake_setting()
    
    # ベイクの実行
    bake_obj.bake_object('DIFFUSE', 'EXTERNAL')
    #bpy.ops.object.bake(type='DIFFUSE', save_mode='EXTERNAL')

    # テクスチャ画像保存
    bake_image.save_render(filepath=texture_path)

    # 作成したテクスチャにフェイクユーザを設定する
    bake_image.use_fake_user = True

    # 指定オブジェクトのマテリアルリストを取得する
    for material_slot in obj.material_slots:
        # スロットのマテリアルを取得する
        target_material = material_slot.material

        # マテリアルが割り当てられているか
        if target_material == None:
            continue

        # 追加した画像ノードを削除する
        tex_sup.delete_node_target(
            material = target_material,
            node = name_mapping[texturenode_name + target_material.name]
        )

def create_baked_model(model_path, output_path, texture_path):
    '''
    ベイクされたモデルを出力するメソッド
    '''
    #クラスインスタンス取得
    obj_sup = ObjectSupport()
    bake_obj = BakeObject()
    tex_sup = TextureSupport()

    # シーンのオブジェクト削除
    obj_sup.delete_target_object("Cube")

    # モデルの読み込み
    bpy.ops.import_scene.gltf(filepath=model_path)

    # 追加モデルのオブジェクト名取得
    model_names = obj_sup.get_add_object_name()

    #追加モデルのオブジェクトごとにベイクを実行
    for model_name in model_names:
        # 追加オブジェクト情報取得
        obj = bpy.data.objects.get(model_name)

        # ベイク処理実行
        create_bake_texture(obj, texture_path, bake_obj, tex_sup)

        # テクスチャ貼り付け
        obj_sup.set_object_texture(obj, texture_path)

    # glbへの変換と出力
    bpy.ops.export_scene.gltf(filepath=output_path)

    print('glbファイルが出力されました。')

def main():
    # パス
    model_path = './input/input.glb'
    output_path = './output/output.glb'
    texture_path = "./output/output.png"

    # 時間計測開始
    time_sta = time.time()

    # ベイクモデル生成
    create_baked_model(model_path, output_path, texture_path)

    # 時間計測終了
    exe_time = time.time()-time_sta
    print(f'実行時間{round(exe_time, 2)}秒')

if __name__ == '__main__':
    main()