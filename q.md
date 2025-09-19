``` python
@asynccontextmanager
    async def page(self, url: str) -> AsyncGenerator[Page, None]:
        """
        새로운 페이지(탭)를 열고 URL로 이동한 후 페이지 객체를 반환하는 컨텍스트 관리자.
        컨텍스트를 벗어나면 페이지는 자동으로 닫힙니다.
        """
        if not self._browser or not self._browser.is_connected():
            raise RuntimeError("Browser is not running. Call launch() first.")

        page = await self._browser.new_page()
        try:
            # networkidle 대신 domcontentloaded를 사용하여 초기 로딩 속도 개선
            await page.goto(url, wait_until="domcontentloaded", timeout=self.timeout * 1000)
            yield page
        finally:
            await page.close()
```
여기서 yield 가 뭐임?

async with 이란?

그럼 사용자는 어떻게 사용해야하고, 사용자가 .page 호출시 라이브러리에서 어떤 일이 일어나는지 정리


Playwright에서 요소(Element)의 정보를 추출하는 핵심 메서드들을 목적별로 정리해 드릴게요. 대부분의 경우 `ElementHandle`보다 **`Locator` 객체를 사용하는 것이 권장**되므로, `Locator` 기준으로 설명하겠습니다.

-----

## 텍스트(Text) 추출

웹 페이지에서 눈에 보이는 글자를 가져오는 가장 기본적인 기능입니다.

  * `all_text_contents()`: **가장 많이 사용됩니다.** 선택된 **모든 요소**의 텍스트를 각각 가져와 \*\*리스트(배열)\*\*로 반환합니다.
  * `text_content()`: 선택된 **첫 번째 요소**의 텍스트만 가져옵니다. `innerText`와 유사하게, CSS 스타일에 의해 숨겨진 텍스트는 포함하지 않습니다. **사용자에게 보이는 텍스트**를 원할 때 적합합니다.
  * `inner_text()`: `text_content()`와 거의 동일하며, 마찬가지로 사용자에게 보이는 텍스트를 반환합니다.
  * `all_inner_texts()`: `all_text_contents()`와 거의 동일하며, 선택된 모든 요소의 보이는 텍스트를 리스트로 반환합니다.

> **💡 `text_content()` vs `textContent` 프로퍼티**
> `text_content()` 메서드는 사람이 보는 텍스트를 반환하지만, `evaluate()`를 통해 직접 접근하는 `element.textContent`는 `<script>`나 `<style>` 태그를 포함한 모든 노드의 텍스트를 가져오므로 결과가 다를 수 있습니다.

-----

## 속성(Attribute) 및 프로퍼티(Property) 추출

HTML 태그에 부여된 `href`, `src`, `class` 같은 속성 값이나, 자바스크립트 객체의 프로퍼티 값을 가져옵니다.

  * `get_attribute('속성이름')`: **지정한 HTML 속성의 값**을 문자열로 반환합니다. 예를 들어 `<a>` 태그의 링크 주소(`href`)나 `<img>` 태그의 이미지 경로(`src`)를 가져올 때 사용합니다.
  * `get_property('프로퍼티이름')`: 요소의 **자바스크립트 프로퍼티 값**을 가져옵니다. 예를 들어, `input` 요소의 현재 값(`value`)이나 체크박스의 체크 상태(`checked`) 같은 동적인 상태를 확인할 때 유용합니다.

> **🤔 속성 vs 프로퍼티?**
> \*\*속성(Attribute)\*\*은 HTML 문서에 직접 작성된 값(`<input value="초기값">`)이고, \*\*프로퍼티(Property)\*\*는 자바스크립트 DOM 객체가 가진 실시간 값(`input.value`는 사용자가 입력하면 바뀜)입니다. 대부분의 경우 속성과 프로퍼티 이름이 같지만, 실시간 상태를 확인하려면 `get_property()`가 더 정확할 수 있습니다.

-----

## HTML 및 입력 값 추출

요소의 내부 HTML 구조나 `<input>`, `<select>` 같은 폼(Form) 요소의 값을 직접 가져옵니다.

  * `inner_html()`: 요소의 **내부 HTML**을 문자열로 반환합니다.
  * `outer_html()`: 요소 **자신을 포함한 HTML**을 문자열로 반환합니다.
  * `input_value()`: `<input>`, `<textarea>`, `<select>` 요소의 \*\*현재 값(value)\*\*을 가져옵니다. `get_attribute('value')`보다 정확한 실시간 값을 제공합니다.
  * `select_option()`: `<select>` 요소에서 \*\*선택된 `<option>`\*\*에 대한 정보를 반환합니다.

-----

## 상태 확인 (Boolean)

요소의 현재 상태를 `True` 또는 `False`로 확인합니다. 조건문(`if`)에 자주 사용됩니다.

  * `is_visible()`: 요소가 **화면에 보이는지** 여부를 확인합니다.
  * `is_hidden()`: 요소가 **화면에 보이지 않는지** 여부를 확인합니다.
  * `is_enabled()`: 요소가 **활성화되어 있는지** (예: 클릭 가능한 버튼) 여부를 확인합니다.
  * `is_disabled()`: 요소가 **비활성화되어 있는지** 여부를 확인합니다.
  * `is_editable()`: 요소가 **편집 가능한 상태인지** (예: `input` 박스) 여부를 확인합니다.
  * `is_checked()`: 라디오 버튼이나 체크박스가 **체크되어 있는지** 여부를 확인합니다.

-----

## 🔮 고급 추출: `evaluate()`

기본 메서드로 추출할 수 없는 복잡한 정보는 `evaluate()`를 사용하여 자바스크립트 코드를 직접 실행해 가져올 수 있습니다.

  * `evaluate('javascript 함수', 인자)`: **선택된 첫 번째 요소**에 대해 브라우저에서 JavaScript 함수를 실행하고 그 결과를 반환합니다.
  * `evaluate_all('javascript 함수', 인자)`: **선택된 모든 요소**에 대해 함수를 실행하고 결과들을 리스트로 반환합니다.

**예시: 요소의 가로(width) 길이와 모든 데이터 속성(`data-*`) 가져오기**

```python
# 첫 번째 요소의 계산된 가로 길이 가져오기
width = await element.evaluate("el => window.getComputedStyle(el).width")

# 모든 요소의 data-id 속성 값들을 리스트로 가져오기
data_ids = await elements.evaluate_all("els => els.map(el => el.dataset.id)")
```





[신분 위장] 🎭 새로운 BrowserContext 생성

평범한 브라우저 탭을 여는 대신, 완전히 격리된 임시 가상 환경(BrowserContext)을 만듭니다.

이때 **UA_POOL**에서 무작위로 **User-Agent**를 하나 고르고, **realistic_headers**를 장착하여 일반 사용자처럼 신분을 위장합니다.

[흔적 지우기] 🤫 STEALTH_SCRIPT 주입

페이지가 열리기 직전, 이 가상 환경에 **STEALTH_SCRIPT**를 주입합니다.

이 스크립트는 Playwright가 남기는 자동화 도구의 흔적(navigator.webdriver 등)을 깨끗이 지워, 웹사이트가 "이 사용자는 로봇이구나"라고 눈치채지 못하게 합니다.

[현장 침투] 🗺️ 페이지 생성 및 이동

위장이 완료된 가상 환경 안에서 드디어 새로운 페이지(탭)를 엽니다.

사용자가 요청한 url로 이동하여 웹사이트에 접속합니다.

[주변에 녹아들기] 🚶‍♂️ simulate_human 실행

페이지 로딩이 끝나면, simulate_human 함수가 실행됩니다.

마우스를 자연스럽게 움직이거나 페이지를 살짝 스크롤하는 등, 실제 사람이 사이트를 둘러보는 듯한 행동을 하여 의심을 피합니다.

[임무 시작] ✅ page 객체 반환

모든 위장과 잠입 준비가 끝나면, 완벽하게 준비된 page 객체를 사용자에게 yield 키워드를 통해 전달합니다.

이제부터 사용자는 이 page 객체를 가지고 원하는 스크레이핑 작업을 수행합니다.

[완전 소멸] 💥 Context 폐기

사용자의 with 블록 안의 코드가 모두 실행되고 나면, finally 구문이 실행됩니다.

페이지 하나만 닫는 것이 아니라, 스파이가 사용했던 모든 것(위장 신분, 쿠키, 활동 기록 등)이 담긴 BrowserContext 자체를 통째로 파기합니다.

따라서 다음 scraper.page() 호출은 또다시 아무런 흔적이 없는 깨끗한 상태에서 새로운 임무를 시작하게 됩니다.