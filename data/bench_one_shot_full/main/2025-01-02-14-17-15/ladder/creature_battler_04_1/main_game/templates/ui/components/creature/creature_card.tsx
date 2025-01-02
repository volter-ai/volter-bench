import * as React from "react"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import withClickable from "@/lib/withClickable.tsx"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  image: string
  hp: number
  maxHp: number
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ uid, name, image, hp, maxHp, className, ...props }, ref) => (
    <Card ref={ref} className={className} {...props}>
      <CardHeader>
        <CardTitle>{name}</CardTitle>
      </CardHeader>
      <CardContent>
        <img src={image} alt={`${name} image`} className="w-full h-auto" />
        <div className="mt-2">
          <div className="text-sm">HP: {hp} / {maxHp}</div>
          <div className="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
            <div
              className="bg-green-500 h-2.5 rounded-full"
              style={{ width: `${(hp / maxHp) * 100}%` }}
            ></div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
)

CreatureCard.displayName = "CreatureCard"
CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
