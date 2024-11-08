import {useCurrentButtons} from "@/lib/useChoices.ts";
import {Play, XCircle} from 'lucide-react'

interface GameStats {
    [key: string]: number;
}

interface GameMeta {
    prototype_id: string;
    category: string;
    [key: string]: string;
}

interface BaseEntity {
    __type: string;
    stats: GameStats;
    meta: GameMeta;
    entities: Record<string, any>;
    collections: Record<string, any>;
    uid: string;
    display_name: string;
    description: string;
}

interface Player extends BaseEntity {
    __type: 'Player';
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
        <div className="relative w-full h-0 pb-[56.25%] bg-gradient-to-b from-slate-900 to-slate-800">
            <div className="absolute inset-0 flex flex-col items-center justify-between p-8">
                <div className="flex-1 flex items-center justify-center">
                    <h1 className="text-6xl font-bold text-white tracking-wider">
                        {props.data?.entities?.player?.display_name || "Game Title"}
                    </h1>
                </div>

                <div className="flex flex-col gap-4 w-full max-w-md">
                    {availableButtonSlugs.includes('play') && (
                        <button
                            onClick={() => emitButtonClick('play')}
                            className="flex items-center justify-center gap-2 w-full py-4 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
                        >
                            <Play className="w-6 h-6" />
                            <span className="text-xl">Play Game</span>
                        </button>
                    )}

                    {availableButtonSlugs.includes('quit') && (
                        <button
                            onClick={() => emitButtonClick('quit')}
                            className="flex items-center justify-center gap-2 w-full py-4 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
                        >
                            <XCircle className="w-6 h-6" />
                            <span className="text-xl">Quit</span>
                        </button>
                    )}
                </div>
            </div>
        </div>
    )
}
