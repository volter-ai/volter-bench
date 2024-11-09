import {useCurrentButtons} from "@/lib/useChoices.ts";
import {Play, XCircle} from 'lucide-react'

interface Player {
    uid: string;
    display_name: string;
    description: string;
}

interface GameUIData {
    entities: {
        player: Player;
    }
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    return (
        <div className="w-full h-full aspect-video bg-gradient-to-b from-slate-900 to-slate-800 flex flex-col items-center justify-between p-8">
            <div className="flex-1 flex items-center justify-center">
                <h1 className="text-6xl font-bold text-white tracking-wider">
                    GAME TITLE
                </h1>
            </div>

            <div className="flex flex-col gap-y-4 items-center mb-12">
                {availableButtonSlugs?.includes('play') && (
                    <button
                        onClick={() => emitButtonClick('play')}
                        className="flex items-center gap-x-2 bg-green-600 hover:bg-green-700 text-white px-8 py-3 rounded-lg text-xl transition-colors"
                    >
                        <Play className="w-5 h-5" />
                        Play Game
                    </button>
                )}

                {availableButtonSlugs?.includes('quit') && (
                    <button
                        onClick={() => emitButtonClick('quit')}
                        className="flex items-center gap-x-2 bg-red-600 hover:bg-red-700 text-white px-8 py-3 rounded-lg text-xl transition-colors"
                    >
                        <XCircle className="w-5 h-5" />
                        Quit
                    </button>
                )}
            </div>
        </div>
    )
}
