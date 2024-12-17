import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"

interface BaseProps {
  uid: string
}

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement>, BaseProps {
  name: string
  image: string
  currentHp: number
  maxHp: number
}

let CustomCard = React.forwardRef<HTMLDivElement, BaseProps & React.ComponentProps<typeof Card>>(
  ({ uid, ...props }, ref) => <Card ref={ref} {...props} />
)

let CustomCardHeader = React.forwardRef<HTMLDivElement, BaseProps & React.ComponentProps<typeof CardHeader>>(
  ({ uid, ...props }, ref) => <CardHeader ref={ref} {...props} />
)

let CustomCardTitle = React.forwardRef<HTMLDivElement, BaseProps & React.ComponentProps<typeof CardTitle>>(
  ({ uid, ...props }, ref) => <CardTitle ref={ref} {...props} />
)

let CustomCardContent = React.forwardRef<HTMLDivElement, BaseProps & React.ComponentProps<typeof CardContent>>(
  ({ uid, ...props }, ref) => <CardContent ref={ref} {...props} />
)

let CustomProgress = React.forwardRef<HTMLDivElement, BaseProps & React.ComponentProps<typeof Progress>>(
  ({ uid, ...props }, ref) => <Progress ref={ref} {...props} />
)

CustomCard = withClickable(CustomCard)
CustomCardHeader = withClickable(CustomCardHeader)
CustomCardTitle = withClickable(CustomCardTitle)
CustomCardContent = withClickable(CustomCardContent)
CustomProgress = withClickable(CustomProgress)

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, image, currentHp, maxHp, ...props }, ref) => {
    return (
      <CustomCard uid={uid} ref={ref} className={cn("w-[350px]", className)} {...props}>
        <CustomCardHeader uid={`${uid}-header`}>
          <CustomCardTitle uid={`${uid}-title`}>{name}</CustomCardTitle>
        </CustomCardHeader>
        <CustomCardContent uid={`${uid}-content`}>
          <div className="flex flex-col gap-4">
            <img
              src={image}
              alt={name}
              className="h-[200px] w-full object-contain"
            />
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>HP</span>
                <span>{`${currentHp}/${maxHp}`}</span>
              </div>
              <CustomProgress uid={`${uid}-progress`} value={(currentHp / maxHp) * 100} />
            </div>
          </div>
        </CustomCardContent>
      </CustomCard>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
