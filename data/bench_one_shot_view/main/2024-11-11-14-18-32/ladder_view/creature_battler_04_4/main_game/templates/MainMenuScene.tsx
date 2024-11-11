import {useCurrentButtons} from "@/lib/useChoices.ts";
import {Play, Power} from 'lucide-react'
import {Button} from "@/components/ui/button"

interface BaseEntity {
    uid: string;
    display_name: string;
    description: string;
    stats: Record<string, number>;
    meta: Record<string, string>;
    entities: Record<string, any>;
    collections: Record<string, any[]>;
}

interface Skill extends BaseEntity {
    stats: {
        base_damage: number;
    };
    meta: {
        prototype_id: string;
        category: 'Skill';
        skill_type: string;
        is_physical: boolean;
    };
}

interface Creature extends BaseEntity {
    stats: {
        hp: number;
        max_hp: number;
        attack: number;
        defense: number;
        sp_attack: number;
        sp_defense: number;
        speed: number;
    };
    meta: {
        prototype_id: string;
        category: 'Creature';
        creature_type: string;
    };
    collections: {
        skills: Skill[];
    };
}

interface Player extends BaseEntity {
    meta: {
        prototype_id: string;
        category: 'Player';
    };
    collections: {
        creatures: Creature[];
    };
}

interface GameUIData extends BaseEntity {
    entities: {
        player: Player;
    };
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    if (!props.data?.entities) {
        return <div className="w-full h-full aspect-video bg-slate-900 flex items-center justify-center">
            <p className="text-white">Loading...</p>
        </div>
    }

    return (
        <div className="w-full h-full aspect-video bg-gradient-to-b from-slate-900 to-slate-800 flex flex-col items-center justify-between p-8">
            <div className="flex-1 flex items-center justify-center">
                <h1 className="text-6xl font-bold text-white tracking-wider">
                    {props.data.display_name || 'CREATURE BATTLE'}
                </h1>
            </div>

            <div className="flex flex-col gap-y-4 items-center mb-12">
                {availableButtonSlugs?.includes('play') && (
                    <Button
                        variant="default"
                        size="lg"
                        onClick={() => emitButtonClick('play')}
                        className="w-48 h-16 text-xl"
                    >
                        <Play className="w-6 h-6 mr-2" />
                        Play Game
                    </Button>
                )}

                {availableButtonSlugs?.includes('quit') && (
                    <Button
                        variant="destructive"
                        size="lg"
                        onClick={() => emitButtonClick('quit')}
                        className="w-48 h-16 text-xl"
                    >
                        <Power className="w-6 h-6 mr-2" />
                        Quit
                    </Button>
                )}
            </div>
        </div>
    )
}
