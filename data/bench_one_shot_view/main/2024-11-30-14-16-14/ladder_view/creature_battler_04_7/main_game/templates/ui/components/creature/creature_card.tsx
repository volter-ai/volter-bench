import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  image: string
  currentHp: number
  maxHp: number
}

interface CustomCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

let CustomCard = React.forwardRef<HTMLDivElement, CustomCardProps>(
  ({ uid, ...props }, ref) => <Card ref={ref} {...props} />
)

let CustomCardContent = React.forwardRef<HTMLDivElement, CustomCardProps>(
  ({ uid, ...props }, ref) => <CardContent ref={ref} {...props} />
)

let CustomCardHeader = React.forwardRef<HTMLDivElement, CustomCardProps>(
  ({ uid, ...props }, ref) => <CardHeader ref={ref} {...props} />
)

let CustomCardTitle = React.forwardRef<HTMLParagraphElement, CustomCardProps>(
  ({ uid, ...props }, ref) => <CardTitle ref={ref} {...props} />
)

let CustomProgress = React.forwardRef<HTMLDivElement, CustomCardProps & { value: number }>(
  ({ uid, ...props }, ref) => <Progress ref={ref} {...props} />
)

CustomCard.displayName = "CustomCard"
CustomCardContent.displayName = "CustomCardContent"
CustomCardHeader.displayName = "CustomCardHeader"
CustomCardTitle.displayName = "CustomCardTitle"
CustomProgress.displayName = "CustomProgress"

CustomCard = withClickable(CustomCard)
CustomCardContent = withClickable(CustomCardContent)
CustomCardHeader = withClickable(CustomCardHeader)
CustomCardTitle = withClickable(CustomCardTitle)
CustomProgress = withClickable(CustomProgress)

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, image, currentHp, maxHp, ...props }, ref) => {
    return (
      <CustomCard uid={uid} ref={ref} className={cn("w-[350px]", className)} {...props}>
        <CustomCardHeader uid={uid}>
          <CustomCardTitle uid={uid}>{name}</CustomCardTitle>
        </CustomCardHeader>
        <CustomCardContent uid={uid}>
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
              <CustomProgress uid={uid} value={(currentHp / maxHp) * 100} />
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
