import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, Power } from 'lucide-react'
import { Button } from "@/components/ui/button"

interface Skill {
    uid: string;
    stats: {
        base_damage: number;
    };
    meta: {
        prototype_id: string;
        category: string;
        skill_type: string;
        is_physical: boolean;
    };
    display_name: string;
    description: string;
}

interface Creature {
    uid: string;
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
        category: string;
        creature_type: string;
    };
    collections: {
        skills: Skill[];
    };
    display_name: string;
    description: string;
}

interface Player {
    uid: string;
    stats: Record<string, never>;
    meta: {
        prototype_id: string;
        category: string;
    };
    entities: {
        active_creature?: Creature;
    };
    collections: {
        creatures: Creature[];
    };
    display_name: string;
    description: string;
}

interface GameUIData {
    entities: {
        player: Player;
    };
    stats: Record<string, never>;
    meta: Record<string, never>;
    collections: Record<string, never>;
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
        <div className="w-full h-full flex flex-col items-center justify-between p-8 bg-gradient-to-b from-slate-800 to-slate-900 aspect-video">
            {/* Title Section */}
            <div className="flex-1 flex items-center justify-center">
                <h1 className="text-6xl font-bold text-white tracking-wider">
                    CREATURE BATTLE
                </h1>
            </div>

            {/* Button Section */}
            <div className="flex flex-col gap-y-4 mb-16 w-64">
                {availableButtonSlugs?.includes('play') && (
                    <Button
                        onClick={() => emitButtonClick('play')}
                        className="w-full h-14 text-xl"
                        variant="default"
                    >
                        <Play className="mr-2 h-6 w-6" />
                        Play Game
                    </Button>
                )}

                {availableButtonSlugs?.includes('quit') && (
                    <Button
                        onClick={() => emitButtonClick('quit')}
                        className="w-full h-14 text-xl"
                        variant="destructive"
                    >
                        <Power className="mr-2 h-6 w-6" />
                        Quit
                    </Button>
                )}
            </div>
        </div>
    )
}
