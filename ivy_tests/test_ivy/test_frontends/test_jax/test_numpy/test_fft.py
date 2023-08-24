# global
from hypothesis import strategies as st

# local
import ivy_tests.test_ivy.helpers as helpers
from ivy_tests.test_ivy.helpers import handle_frontend_test


# fft
@handle_frontend_test(
    fn_tree="jax.numpy.fft.fft",
    dtype_values_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("complex"),
        num_arrays=1,
        min_value=-1e5,
        max_value=1e5,
        min_num_dims=1,
        max_num_dims=5,
        min_dim_size=1,
        max_dim_size=5,
        allow_inf=False,
        large_abs_safety_factor=2.5,
        small_abs_safety_factor=2.5,
        safety_factor_scale="log",
        valid_axis=True,
        force_int_axis=True,
    ),
    n=st.integers(min_value=2, max_value=10),
    norm=st.sampled_from(["backward", "ortho", "forward", None]),
)
def test_jax_numpy_fft(
    dtype_values_axis, n, norm, frontend, backend_fw, test_flags, fn_tree, on_device
):
    dtype, values, axis = dtype_values_axis
    helpers.test_frontend_function(
        input_dtypes=dtype,
        frontend=frontend,
        backend_to_test=backend_fw,
        test_flags=test_flags,
        fn_tree=fn_tree,
        on_device=on_device,
        a=values[0],
        n=n,
        axis=axis,
        norm=norm,
        atol=1e-02,
        rtol=1e-02,
    )


# fftshift
@handle_frontend_test(
    fn_tree="jax.numpy.fft.fftshift",
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("valid"), shape=(4,), array_api_dtypes=True
    ),
)
def test_jax_numpy_fftshift(
    dtype_and_x, backend_fw, frontend, test_flags, fn_tree, on_device
):
    input_dtype, arr = dtype_and_x
    helpers.test_frontend_function(
        input_dtypes=input_dtype,
        frontend=frontend,
        backend_to_test=backend_fw,
        test_flags=test_flags,
        fn_tree=fn_tree,
        on_device=on_device,
        test_values=True,
        x=arr[0],
        axes=None,
    )


@st.composite
def x_and_ifftn(draw):
    min_fft_points = 2
    dtype = draw(helpers.get_dtypes("complex"))
    x_dim = draw(
        helpers.get_shape(
            min_dim_size=2, max_dim_size=100, min_num_dims=1, max_num_dims=4
        )
    )
    x = draw(
        helpers.array_values(
            dtype=dtype[0],
            shape=tuple(x_dim),
            min_value=-1e-10,
            max_value=1e10,
        )
    )
    axes = draw(
        st.lists(
            st.integers(0, len(x_dim) - 1), min_size=1, max_size=len(x_dim), unique=True
        )
    )
    norm = draw(st.sampled_from(["forward", "ortho", "backward"]))
    s = draw(
        st.lists(
            st.integers(min_fft_points, 256), min_size=len(axes), max_size=len(axes)
        )
    )
    return dtype, x, s, axes, norm


# ifftn
@handle_frontend_test(
    fn_tree="jax.numpy.fft.ifftn",
    dtype_values_axes_norm=x_and_ifftn(),
)
def test_jax_numpy_ifftn(
    dtype_values_axes_norm,
    frontend,
    backend_fw,
    test_flags,
    fn_tree,
    on_device,
):
    dtype, a, s, axes, norm = dtype_values_axes_norm

    helpers.test_frontend_function(
        input_dtypes=dtype,
        frontend=frontend,
        test_flags=test_flags,
        backend_to_test=backend_fw,
        on_device=on_device,
        fn_tree=fn_tree,
        a=a,
        s=s,
        axes=axes,
        norm=norm,
    )
