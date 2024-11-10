import {useCurrentButtons} from "@/lib/useChoices.ts";
import {Play, Power} from 'lucide-react'

interface Stats {
    [key: string]: number;
}

interface Meta {
    prototype_id: string;
    category: string;
    [key: string]: string;
}

interface BaseEntity {
    __type: string;
    uid: string;
    display_name: string;
    description: string;
    stats: Stats;
    meta: Meta;
    entities: Record<string, any>;
    collections: Record<string, any[]>;
}

interface Skill extends BaseEntity {
    __type: 'Skill';
    stats: {
        base_damage: number;
    };
    meta: {
        skill_type: string;
        is_physical: boolean;
    } & Meta;
}

interface Creature extends BaseEntity {
    __type: 'Creature';
    stats: {
        hp: number;
        max_hp: number;
        attack: number;
        defense: number;
        sp_attack: number;
        sp_defense: number;
        speed: number;
    };
    collections: {
        skills: Skill[];
    };
}

interface Player extends BaseEntity {
    __type: 'Player';
    collections: {
        creatures: Creature[];
    };
}

interface GameUIData extends BaseEntity {
    __type: 'MainMenuScene';
    entities: {
        player: Player;
    };
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    if (!props?.data) {
        return null;
    }

    return (
        <div className="relative w-full h-full aspect-video bg-gradient-to-b from-slate-900 to-slate-800 flex flex-col items-center justify-between p-8 overflow-hidden">
            <div className="flex-1 flex items-center justify-center">
                <h1 className="text-6xl font-bold text-white tracking-wider animate-fade-in">
                    {props.data?.display_name || "CREATURE BATTLE"}
                </h1>
            </div>

            <div className="flex flex-col gap-y-4 items-center mb-12 w-full max-w-md">
                {availableButtonSlugs?.includes('play') && (
                    <button
                        onClick={() => emitButtonClick('play')}
                        className="w-full flex items-center justify-center gap-x-2 bg-green-600 hover:bg-green-700 text-white px-8 py-4 rounded-lg text-xl font-semibold transition-colors duration-200"
                    >
                        <Play className="w-6 h-6" />
                        Play Game
                    </button>
                )}

                {availableButtonSlugs?.includes('quit') && (
                    <button
                        onClick={() => emitButtonClick('quit')}
                        className="w-full flex items-center justify-center gap-x-2 bg-red-600 hover:bg-red-700 text-white px-8 py-4 rounded-lg text-xl font-semibold transition-colors duration-200"
                    >
                        <Power className="w-6 h-6" />
                        Quit
                    </button>
                )}
            </div>
        </div>
    )
}
