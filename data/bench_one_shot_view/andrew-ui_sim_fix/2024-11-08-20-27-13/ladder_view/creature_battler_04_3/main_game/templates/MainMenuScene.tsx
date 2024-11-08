import {useCurrentButtons} from "@/lib/useChoices.ts";
import {Play, XCircle} from 'lucide-react'

interface Stats {
    [key: string]: number;
}

interface Meta {
    prototype_id: string;
    category: string;
    [key: string]: string;
}

interface Skill {
    __type: string;
    stats: {
        base_damage: number;
    };
    meta: Meta;
    entities: Record<string, unknown>;
    collections: Record<string, unknown>;
    uid: string;
    display_name: string;
    description: string;
}

interface Creature {
    __type: string;
    stats: {
        hp: number;
        max_hp: number;
        attack: number;
        defense: number;
        sp_attack: number;
        sp_defense: number;
        speed: number;
    };
    meta: Meta;
    entities: Record<string, unknown>;
    collections: {
        skills: Skill[];
    };
    uid: string;
    display_name: string;
    description: string;
}

interface Player {
    __type: string;
    stats: Stats;
    meta: Meta;
    entities: Record<string, unknown>;
    collections: {
        creatures: Creature[];
    };
    uid: string;
    display_name: string;
    description: string;
}

interface GameUIData {
    __type: string;
    stats: Stats;
    meta: Record<string, unknown>;
    entities: {
        player: Player;
    };
    collections: Record<string, unknown>;
    uid: string;
    display_name: string;
    description: string;
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
                    {props.data?.display_name || "GAME TITLE"}
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
