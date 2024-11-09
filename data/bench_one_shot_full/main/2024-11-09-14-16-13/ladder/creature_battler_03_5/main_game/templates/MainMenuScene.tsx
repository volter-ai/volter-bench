import {useCurrentButtons} from "@/lib/useChoices.ts";
import {Play, Power} from 'lucide-react'

interface ExamplePlayer {
    uid: string,
    stats: {
        stat1: number,
    },
}

interface GameUIData {
    entities: {
        player: ExamplePlayer
    }
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    return (
        <div className="w-full h-full aspect-video bg-slate-900 flex flex-col items-center justify-between p-8">
            <div className="flex-1 flex items-center justify-center">
                <h1 className="text-6xl font-bold text-white tracking-wider">
                    Monster Battle
                </h1>
            </div>

            <div className="flex flex-col gap-4 mb-16 w-64">
                {availableButtonSlugs.includes('play') && (
                    <button
                        onClick={() => emitButtonClick('play')}
                        className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-slate-700 hover:bg-slate-600 text-white rounded-md text-xl transition-colors"
                    >
                        <Play className="w-5 h-5" />
                        <span>Play Game</span>
                    </button>
                )}

                {availableButtonSlugs.includes('quit') && (
                    <button
                        onClick={() => emitButtonClick('quit')}
                        className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-slate-700 hover:bg-slate-600 text-white rounded-md text-xl transition-colors"
                    >
                        <Power className="w-5 h-5" />
                        <span>Quit</span>
                    </button>
                )}
            </div>
        </div>
    )
}
